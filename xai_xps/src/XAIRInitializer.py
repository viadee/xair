import json
import numpy as np
import os
import pandas as pd
import sys
from Utils import get_logger, get_config, get_ante_config
from XAIRecommenderVariables import XAIRecommenderInput, XAIRecommenderOutput
from argparse import Namespace
from pydoc import locate
from skfuzzy import control as ctrl
from types import SimpleNamespace


class XAIRInitializer(object):

    def __init__(self, config_file_path=None, verbose=True):
        """
        Initialize XAIRInitializer to prepare resouces needed for XAIRecommender.

        @param config_file_path: Path to config file where resouces are mentioned
        @param verbose: Whether status should be logged or not
        """

        self.config = get_config(config_file_path)

        # get logger
        self.logger = get_logger(__name__, activate_console_logs=verbose)

    def initialize(self,
                   reload=False
                   ):
        """
        Check if necessary config files are available, create missing system config files and load
        ratings, rules, antecedents and consequents for XAIRecommender.

        @param reload: Whether or not rules, antecedents and consequents should be reloaded from config files
        """

        # if no json file of ante_config is available, generate from antecedent_config.py
        try:
            self.ante_config = get_ante_config(reload=reload)
            with open(self.config.resource_files.consequent_config) as f:
                self.conse_config = json.load(f)
        except:
            # if no json file of ante_config is available, generate from antecedent_config.py
            self.logger.info("No JSON of antecedent config available. Creating default one.")

        # check input types
        self.input_types = {a: v["dtypes"]["crisp"] for a, v in self.ante_config.items() if "dtypes" in v}
        assert None not in self.input_types.values(), "Invalid input type in config"

        # necessary: ratings (bool and crisp), antecedent config, consequent config
        # if one file is missing there might be inconsistencies, so reload everything
        load_files = ["rating_bool", "rating_fuzzy"]
        not_available = [(x, os.path.isfile(self.config.resource_files.__dict__[x])) for x in load_files]
        assert [a[1] for a in not_available].count(
            False) == 0, "Required ratings, rules, antecedents or consequents are not available ({}). Creating ALL components programmatically.".format(
            [a[0] for a in not_available if a[1] == False])

        # if reload whished or antecedents/consequents/rules not available
        check_files = [(x, os.path.isfile(self.config.resource_files.__dict__[x])) for x in
                       ["antecedents", "consequents"]]
        if reload or [a[1] for a in check_files].count(False) > 0:
            self.logger.info(
                "Required rules, antecedents or consequents are not available ({}). Creating them from config files.".format(
                    [a[0] for a in check_files if a[1] == False]))

            # throw error if CSVs are invalid
            self.__check_exclusion_criteria()
            self.__check_fuzzy_criteria()

            # if no ante or con npy is available, load them from config
            self.antecedents, self.consequents = self.__load_variables()

            # for frontend: load antecedents and save to separate json file
            self.__save_frontend_config()

            # activate new rules load since they got created above
            reload = True
        else:
            self.logger.info("Loading saved antecedents and consequents from files.")
            self.antecedents = np.load(self.config.resource_files.antecedents, allow_pickle=True).item()
            self.consequents = np.load(self.config.resource_files.consequents, allow_pickle=True).item()

        # separate reload of rules from rest, since they might be extended
        if not os.path.isfile(self.config.resource_files.rules) or reload:
            self.logger.info("Reloading rules by extracting them from rating CSVs.")
            # reloads and saves rules
            self.__load_rules_from_rating()

    def __save_frontend_config(self):
        """
            Save input config file used in frontend according to antecedent config file
        """
        dir = self.config.resource_files.frontend_input_config
        self.logger.info(f"Updating configuration for frontend inputs to: {dir}")
        input_config_frontend = {k: {"label": v["label"], "config": v["frontend"]} for k, v in self.ante_config.items()
                                 if
                                 "frontend" in v}

        os.makedirs(os.path.dirname(dir), exist_ok=True)
        with open(dir, "w") as outfile:
            json.dump(input_config_frontend, outfile)

    def __check_fuzzy_criteria(self, criteria_df=None):
        """
            Validate fuzzy criteria rating DataFrame
        """

        # except disable default rating (standalone_impact == False): criteria for which methods should not be rated (e.g. Performance Prefs)
        crits = [v["label"] for v in self.ante_config.values() if
                 v["type"] == "rating_criteria" and v["rules"]["standalone_impact"]]

        if criteria_df is None:
            self.logger.info("Checking fuzzy rating from file '{}'".format(self.config.resource_files.rating_fuzzy))
            criteria_df = pd.read_csv(self.config.resource_files.rating_fuzzy, index_col=[0, 1])

        # check if fuzzy rating is consistent with exclusion criteria
        # since there is no default rating for every single criteria, ratings must be > criteria in config
        diff = [x for x in list(set(crits) - set(criteria_df.index.levels[0]))]
        assert 0 == len(
            diff), "XAI methods must be rated for all {}  criteria. Criteria '{}' is inconsistent in config and rating table.".format(
            len(crits), diff)

        # assert all XAI methods are rated
        diff = set([v["label"] for v in self.conse_config.values()]).symmetric_difference(
            set(criteria_df.columns.values))  # starting at 1 since it's a multi index
        assert 0 == len(
            diff), "All XAI methods must be rated for all criteria. Please check alternative '{}' ".format(
            diff)
        self.logger.info("-- Given criteria ratings valid.")

    def __check_exclusion_criteria(self):
        """
            Validate exclusion criteria rating DataFrame
        """
        exclusion_criteria = [k for k, v in self.ante_config.items() if v["type"] == "exclusion_criteria"]

        self.logger.info(
            "Loading exclusion criteria rating from file '{}'".format(self.config.resource_files.rating_fuzzy))

        d = pd.read_csv(self.config.resource_files.rating_bool, index_col=[0])

        # check if bool rating is consistent with exclusion criteria
        diff = set(exclusion_criteria).symmetric_difference(set(d.index))
        assert 0 == len(
            diff), "XAI methods must be rated for all {} exclusion criteria. Exclusion criteria '{}' is inconsistent in config and rating table.".format(
            len(exclusion_criteria), diff)

        # assert all XAI methods are rated
        diff = set([x["label"] for x in  self.conse_config.values()]).symmetric_difference(
            set(d.columns.values))
        assert 0 == len(
            diff), "XAI methods of rating is different than given XAI methods in config. All XAI methods must be rated " \
                   "for all exclusion criteria and all rated methods must be listed there. Please check alternative '{}' ".format(
            diff)

        self.logger.info("-- Given exclusion criteria valid.")

    def __get_ante_name_by_label(self, label):
        """
            @returns Name of antecedent with given label
        """
        try:
            return [x.name for x in self.antecedents.values() if x.label == label][0]
        except:
            raise KeyError(
                f"The required label '{label}' is not available in the given configuration for the antecedents.\n "
                f"Please check consistency of rating DataFrame and Antecedent config.")

    def __get_consequent_by_label(self, label):
        """
            @returns Name of consequent with given label
        """
        return [x.variable for x in self.consequents.values() if x["label"] == label][0]

    def __load_rules_from_rating(self):
        # TODO wenn ratings vorhanden, keine neuen erstellen
        # wenn nicht, standard erstellen
        # custom regeln nur bauen, wenn erwuenscht
        """
            Extracts rules from rating DataFrame with criteria per row and XAI method as alternatives
        """

        import pickle
        import re
        from skfuzzy.control.term import TermAggregate

        def rate(antecedent_name, rating):
            """
                Rate antecedent

                @returns Rated antecedent
            """
            try:
                a = an.__dict__[antecedent_name]
                return a[rating]
            except:
                self.logger.error("Antecedent '{}[{}]' not available.".format(antecedent_name, rating))

        def extract_rules(df, input_name, weights_array=None, weights_axis=0):
            """
            Create rules for Antecedent "input_name" out of DataFrame

            @param df: DataFrame to extract ratings from
            @param input_name: Name of criterion (Antecedent)
            @param weights_array: List with single value or list of lists(for rows if axis=0, for cols if axis=1))
                                    can be added to weight rules, otherwise weight = 1
            @param weights_axis: Axis to which to apply weights to (0 = rows, 1 = cols)

            @returns List of rules from DataFrame
            """

            def _get_weights(weights_array, weights_axis):
                """
                Define weight according to rating in alternatives DataFrame and assign list of weights or single
                weight to row for weighted DataFrame

                @param weights_array: array with weights
                @param weights_axis: Define axis for which to apply weights.
                                        If 0, fill rows with values (per criterion value).
                                        If 1: fill columns with weight value (per XAI method)
                @returns DataFrame with weights
                """
                if isinstance(weights_array, float):
                    return pd.DataFrame(np.ones(df.shape) * weights_array, columns=df.columns.values, index=df.index)
                if len(weights_array) == 1:
                    return pd.DataFrame(np.ones(df.shape) * weights_array[0], columns=df.columns.values, index=df.index)

                if weights_axis == 0:
                    # fill rows with values (per criterion value)
                    assert len(weights_array) == len(
                        df.index), "If weight axis == 0, length of weights_array must match number of rows in df"
                    weights = []
                    [weights.append(np.ones(len(df.columns.values)) * w) for w in weights_array]

                    weights_df = pd.DataFrame(weights, columns=df.columns.values, index=df.index)
                else:
                    # fill alternative with weight value
                    assert len(weights_array) == len(
                        df.columns.values), "If weight axis == 1, length of  ({}) must match number of columns in df ({})".format(
                        len(weights_array), len(
                            df.columns.values))
                    d = {}
                    for idx, c in enumerate(df.columns.values):
                        d[c] = [weights_array[idx]] * len(df.index)

                    weights_df = pd.DataFrame(d, columns=df.columns.values, index=df.index)

                return weights_df

            rules = []

            if weights_array is None:
                weights = pd.DataFrame(np.ones(df.shape), columns=df.columns.values, index=df.index)
            else:
                weights = _get_weights(weights_array, weights_axis)
                self.logger.debug("Using custom weights for input {}: {}".format(input_name, weights_array))

            # iterate over criteria
            for i, row in df.iterrows():

                # check if row has values
                if row.isnull().sum() == len(row.values):
                    self.logger.info(
                        "Row {} not containing any values. Skip adding rule for {}[{}]".format(i, input_name, i))
                else:
                    # create rule with no consequences if criterion value is irrelevant for all methods
                    # check if row just contains irrelevant values
                    if row.values.tolist().count("-") == len(row.values):
                        res = (cn.noop[rn.VH])
                    else:
                        res = ()
                        col_count = 0
                        # create consequent for rules for every alternative
                        # zip method and rating
                        for c, rating in zip(df.columns.values, row):
                            if col_count == len(row):
                                col_count = 0

                            c = self.__get_consequent_by_label(c)
                            # [con.variable for con in self.consequents.values() if con.label == c][0]

                            # check if val is string of rating joint with weight
                            if "%" in rating:
                                rating, weight = rating.split("%")
                                res = res + ((c[rating] % float(weight)),)
                            else:
                                # add rating if not irrelevant
                                if rating != rn.irrelevant:
                                    w = float(weights.iloc[np.where(df.index == i)[0][0], col_count])
                                    res = res + ((c[rating] % w),)  # % w

                            col_count += 1
                    if rate(input_name, i) is not None:
                        rules.append(ctrl.Rule(rate(input_name, i), res))
                        # if res is not (cn.noop[rn.VH]):
                        #    self.logger.info("Adding rule: ", rules[-1])
            return rules

        def extract_rules_with_prereq(df, input_name, prereq_name, prereq_val=None, weights_array=None, weights_axis=0):
            """
            Create rules for Antecedent "input_name" out of DataFrame,
            adding Antecedent "prereq_name" with value "prereq_val" to every rule.

            @param df: DataFrame to extract ratings from
            @param input_name: Name of criterion (Antecedent)
            @param prereq_name: Name of prerequisite (Antecedent)
            @param prereq_val: Value of prerequisite. If None, same value as the Antecedent (row index of DataFrame)is used
                            Default: none
            @param weights_array: List with single value or list of lists(for rows if axis=0, for cols if axis=1))
                    can be added to weight rules, otherwise weight = 1
            @param weights_axis: Axis to which to apply weights to (0 = rows, 1 = cols)

            @returns Rule with added prerequisite
            """

            cur_rules = extract_rules(df, input_name, weights_array, weights_axis)
            prereq_rules = []

            for rule in cur_rules:
                # can only be a single antecedent if extracted from dataframe
                cur_ante = rule.antecedent_terms[0]
                cur_cons = rule.consequent

                prereq_val = prereq_val if prereq_val is not None else re.search(r"\[([A-Za-z]+)]",
                                                                                 cur_ante.full_label).group(1)

                # TODO check if prereq val is valid for prereq_name

                prereq_rules.append(ctrl.Rule(rate(prereq_name, prereq_val) & cur_ante, cur_cons))
            return prereq_rules

        def __assert_rating_valid(name, rating):
            """
                Assert that criterion is available and that rating is valid
            """
            try:
                if name in self.antecedents.keys():
                    ratings = self.antecedents[name].rating
                else:
                    ratings = self.consequents[name].rating

                assert rating in ratings, "Invalid rating for given Variabe: {}: {}".format(name, rating)
            except:
                self.logger.error("Given variabe name {} is neither a antecedent, nor a consequent".format(name))

        ###########################################

        # Define weights for reduced criterion importance
        red_weight = self.config.criteria.weight_reduced_general

        # ratings
        rating_5 = [r for r in self.config.ratings if len(r) == 5][0]
        rating_dict = dict(zip(rating_5, rating_5))
        rating_dict.update({
            "irrelevant": "-",
            "NO": "False",
            "YES": "True",
        })
        rn = Namespace(**rating_dict)

        # consequents
        # add noop to namespace
        consequent_vals = {k: v.variable for k, v in self.consequents.items()}
        noop = XAIRecommenderOutput("noop", "NOOP", self.config.fuzzy.universes.u_10,
                                    self.config.fuzzy.mem_funcs.tri.u10_5,
                                    rating=["VL", "L", "M", "H", "VH"
                                            ],
                                    defuzzify_method=
                                    self.config.fuzzy.defuzzify_method)
        consequent_vals["noop"] = noop.variable
        cn = Namespace(**consequent_vals)
        an = Namespace(**{k: v.variable for k, v in self.antecedents.items()})

        # todo or take only fuzzy arguments in csv and load others from config?

        self.logger.info("Loading fuzzy rating from file '{}'".format(self.config.resource_files.rating_fuzzy))
        d = pd.read_csv(self.config.resource_files.rating_fuzzy, index_col=[0, 1])

        crits = [v["label"] for v in self.ante_config.values() if
                 v["type"] == "rating_criteria" and v["rules"]["standalone_impact"]]

        crits_t = [v["label"] for v in self.ante_config.values() if
                 v["type"] == "rating_criteria"]

        assert len([c for c in crits if c not in d.index.levels[
            0]]) == 0, f"Not all fuzzy criteria given in fuzzy rating dataframe! ({[c for c in crits if c not in d.index.levels[0]]})"

        # drop rows with only NaN values
        d = d.dropna(thresh=len(d.columns.values))

        ############## Extract rules ##############

        rules = set()

        # initial rule: rate all with 'M'
        rules.add(ctrl.Rule(rate("init", rn.NO), (
            cn.pdp_ice[rn.M], cn.ale[rn.M], cn.pfi[rn.M], cn.shap[rn.M], cn.anchors[rn.M], cn.cfproto[rn.M],
            cn.noop[rn.M])))
        rules.add(ctrl.Rule(rate("init", rn.YES), (
            cn.pdp_ice[rn.M], cn.ale[rn.M], cn.pfi[rn.M], cn.shap[rn.M], cn.anchors[rn.M], cn.cfproto[rn.M],
            cn.noop[rn.M])))

        def __get_visualization_weights(lower=True):
            """
                Rate visualization methods with reduced weight

                @param lower: If true, rate isualization methods with reduced weight, if False, rate others with reduced
                @return weights array to apply to rules
            """
            weight_vis = red_weight if lower else 1
            weight_other = 1 if lower else red_weight

            return [weight_vis if x["visualization"] == 1 and x["label"] != "NOOP" else weight_other for x
                           in self.conse_config.values()]


        # same weight for all memberships
        # defined per row
        for crit in crits:
            if "foi" in crit.lower():
                # if "foi" is in criteria label:
                # rate visualisation methods with 1, everything else with 0.7
                weights = __get_visualization_weights(lower=False)
            elif " ".join((crit.lower(), "foi")) in [val["label"].lower() for val in self.ante_config.values()]:
                # if criteria is rated for FOI as well adapt weight array
                weights = __get_visualization_weights(lower=True)
            else:
                weights = [1] * len(self.conse_config)

            abbr = self.__get_ante_name_by_label(crit)
            # [x.name for x in self.antecedents.values() if x.label == crit][0]
            # self.logger.info("Rating criteria '{}' with weights: {}".format(abbr, weights))
            rules.update(extract_rules(d.loc[crit], abbr, weights, weights_axis=1))

        ############## Custom rules with prerequisite ##############

        # TODO find a way how to easily configure this

        with open(self.config.resource_files.custom_rules) as f:
            custom_config = json.load(f)
        custom_rules = []

        # adding prerequisites to given criteria in rating table
        ratings_prereq = dict(custom_config["use_ratings_with_prereq"])

        # check if  rating for criteria is available
        diff = set(ratings_prereq.keys()) - (set([self.__get_ante_name_by_label(label) for label in d.index.levels[0]]))
        assert 0 == len(
            diff), "XAI methods must be rated for all {} criteria used in custom rules. Rating for '{}' is missing in rating table.".format(
            len(ratings_prereq), diff)
        try:
            for k, val in ratings_prereq.items():
                # duration call
                # add rules for perf_pref H with weight 1
                label = self.antecedents[k].label
                assert label in d.index.levels[
                    0], "'{}' not in given rating table, but used in custom rules!".format(label)

                for rule in val:
                    __assert_rating_valid(rule["prereq_name"], rule["prereq_val"])
                    if "foi" in rule["prereq_name"]:
                        # weights per column (axis=1)
                        weights = __get_visualization_weights(lower=False)
                        weights_axis = 1
                    try:
                        # weights per row (axis=0)
                        r_weights = rule["weights"]
                        weights_axis = 0
                    except KeyError:
                        r_weights = weights

                    [custom_rules.append(r) for r in
                     extract_rules_with_prereq(d.loc[label], k, prereq_name=rule["prereq_name"],
                                               weights_array=r_weights, weights_axis=weights_axis,
                                               prereq_val=rule["prereq_val"])]
        except AttributeError as e:
            self.logger.error("Error in getting rules with prerequisites from custom rule file.")

        for rule in list(custom_config["custom_rules"]):
            # getting antecedents
            cur_ante = ()
            for a in rule["antecedent"]:
                # done in method
                # assert_rating_valid(a["name"], a["value"])
                cur_ante = cur_ante + (rate(a["name"], a["value"]),)

            # getting consequents
            cur_cons = ()
            for c in rule["consequent"]:
                __assert_rating_valid(c["name"], c["value"])
                cons = self.consequents[c["name"]].variable
                rating = c["value"]
                try:
                    cur_cons = cur_cons + ((cons[rating] % c["weight"]),)
                except KeyError:
                    # if no weight is mentioned, take weight of 1
                    cur_cons = cur_cons + ((cons[rating] % 1),)

            # join all antecedents
            if len(cur_ante) == 0:
                raise ValueError("No antecedent is given in custom rule config for rule: ".format(rule))
            elif len(cur_ante) == 1:
                custom_rules.append(ctrl.Rule((rate("corr", rn.H) & rate("discr", rn.H)), cur_cons))
            else:
                term = cur_ante[0]
                for i in range(1, len(cur_ante), 1):
                    term = TermAggregate(term, cur_ante[i], "and")

                custom_rules.append(ctrl.Rule(term, cur_cons))

        rules.update(custom_rules)

        rule_path = self.config.resource_files.rules
        self.logger.info(
            "Saving {} Rules to '{}' (including NOOP rules)...".format(len(rules), rule_path))

        with open(rule_path, "wb") as f:
            pickle.dump(rules, f)

    def __load_variables(self):
        """
        Load default Antecedents and Consequents.

        @param custom_antecedents: Dict of XAIRecommenderInput (criteria to rate XAI Methods) to add to default ones. Default criterion with same key will be replaced.
        @param custom_consequents: Dict of XAIRecommenderOutput (AI Methods) to add to default ones. Default method with same key will be replaced.

        @returns Antecedents and Consequents used by the XAIRecommender
        """


        ante_dir = self.config.resource_files.antecedents
        conse_dir = self.config.resource_files.consequents

        # remove other (FOI, init) and exclusion criteria from antecedent list
        no_fuzzy_input = [k for k, v in self.ante_config.items() if
                          v["type"] == "other" or v["type"] == "exclusion_criteria"]

        antecedents = dict()

        # antecedents contains all criteria, so don't create exclusion criteria
        for k, v in self.ante_config.items():
            if k not in no_fuzzy_input:
                antecedents[k] = XAIRecommenderInput(k, v["label"], v["universe"], v["mem_funcs"], v["rating"])

        self.logger.info("Saving Antecedents ({}) to {}'...".format(antecedents.keys(), ante_dir))
        os.makedirs(os.path.dirname(ante_dir), exist_ok=True)
        with open(ante_dir, 'wb') as f:
            np.save(f, antecedents)

        consequents = dict()

        for k, v in self.conse_config.items():
            consequents[k] = XAIRecommenderOutput(k, v["label"], self.config.fuzzy.universes.u_10,
                                                  self.config.fuzzy.mem_funcs.tri.u10_5,
                                                  rating=["VL", "L", "M", "H", "VH"
                                                          ],
                                                  defuzzify_method=
                                                  self.config.fuzzy.defuzzify_method)

        self.logger.info("Saving Consequents ({}) to {}'...".format(consequents.keys(), conse_dir))

        os.makedirs(os.path.dirname(conse_dir), exist_ok=True)
        with open(conse_dir, 'wb') as f:
            np.save(f, consequents)


        return antecedents, consequents
