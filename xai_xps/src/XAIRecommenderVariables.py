import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
import skfuzzy as fuzz
import sys
from Utils import get_logger, get_config, get_ante_config, plot_membership
from cerberus import Validator
from skfuzzy import control as ctrl
from skfuzzy.control.controlsystem import CrispValueCalculator

sys.path.append("./../")
from resources.config.antecedent_config import RATING_METHODS


class XAIRecommenderVariable(object):
    """
        Class with helper functions for Recommender antecedents and consequents.
    """

    def __init__(self, name: str, label: str, mem_type: list, rating: list):

        self.mem_type = mem_type
        self.rating = rating
        self.name = name  # equals self.variable.label
        self.label = label

        assert len(mem_type) == len(
            rating), "Variable {}: Number of memberships({}) must be equal to number of rating ({})".format(name, len(
            mem_type), len(rating))

        # self.ctrl.antecedent = ctrl.Antecedent(self.universe, self.name)
        self.mem_funcs = self.__set_mem_functions()

    def __set_mem_functions(self):
        """
            Updates membership functions within variable (ante/dec)
        """
        mems = {}
        a_mem_func = [fuzz.trimf(self.variable.universe, r) if len(r) == 3 else fuzz.trapmf(self.variable.universe, r)
                      for r in self.mem_type]

        for i, f in enumerate(a_mem_func):
            self.variable[self.rating[i]] = f
            mems.update({self.rating[i]: f})
        return mems

    def plot_membership_function(self, colors=["b", "g", "r", "y", "m"], figsize=(8, 2), savedir=None):
        f = plt.figure(figsize=figsize)
        ax = f.add_subplot(111)
        # universe, membership function, color
        for mem, label, color in zip(self.mem_funcs.values(), list(self.mem_funcs.keys()), colors):
            ax.plot(self.variable.universe, mem, color, linewidth=1.5, label=label)

        # Hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')

        plt.ylabel('Fuzzy membership')
        plt.xlabel('Universe variable')

        ax.set_title(self.variable.label)
        ax.legend()

        # save if dir is not None
        if savedir is not None:
            plt.tight_layout()
            plt.savefig(os.path.join(savedir, "{}.png".format(self.variable.label)))

    def get_membership_values(self, val):
        mems = {}
        for idx, m in enumerate(self.mem_funcs.values()):
            mems[self.rating[idx]] = np.around(fuzz.interp_membership(self.variable.universe, m, val), 3)
        return mems

    def __getitem__(self, key):
        return getattr(self, key)

    def __new__(cls, *args, **kwargs):
        if cls is XAIRecommenderVariable:
            raise TypeError(
                "XAIRecommenderVariable class may not be instantiated directly. Please consider XAIRecommenderInput or XAIRecommenderOutput")
        return super().__new__(cls)  # , *args, **kwargs)


# class XAIRecommenderInput(name: str, universe: list, mem_type: list, rating=None):
class XAIRecommenderInput(XAIRecommenderVariable):
    """
        Antecedent Wrapper Class
        Parameters:
        ----------
            name: Name of antecedent
            universe: Universe of discourse
            mem_type: List of membership values
    """

    def __init__(self, name: str, label: str, universe: np.ndarray, mem_type: list, rating=[
        "L",
        "M",
        "H"
    ]):
        self.variable = ctrl.Antecedent(universe, name)
        # self.mem_funcs = self.__set_mem_functions()
        # super().__init__(name, universe, mem_type)
        super().__init__(name, label, mem_type, rating)

    def __str__(self):
        mems = set([len(t) for t in self.mem_type])
        m = ["triangular"] if 3 in mems else []
        m += ["trapezoidal"] if 4 in mems else ["?"]
        return "Antecedent '{}': Universe: [{} - {}],  Membership type: {}, Ratings: {}".format(self.variable.label,
                                                                                                self.variable.universe[
                                                                                                    0],
                                                                                                self.variable.universe[
                                                                                                    -1], m, self.rating)


# class XAIRecommenderInput(name: str, universe: list, mem_type: list, rating=None):
class XAIRecommenderOutput(XAIRecommenderVariable):
    """
        Class with helper functions for Recommender antecedents and decedents.
        For Consequent, name equals label
    """

    def __init__(self, name: str, label: str, universe: np.ndarray, mem_type: list, rating=["VL", "L", "M", "H", "VH"
                                                                                            ],
                 defuzzify_method='centroid') -> object:
        self.variable = ctrl.Consequent(universe, label, defuzzify_method)

        super().__init__(name, label, mem_type, rating)

    def __str__(self):
        return "Consequent '{}':  Universe: [{} - {}],  Ratings: {}, Defuzzify method: {}".format(self.variable.label,
                                                                                                  self.variable.universe[
                                                                                                      0],
                                                                                                  self.variable.universe[
                                                                                                      -1], self.rating,
                                                                                                  self.variable.defuzzify_method)


class XAIRecommenderControlSystem(ctrl.ControlSystem):

    def __init__(self, rules, config_file_path):

        self.logger = get_logger(__name__, activate_console_logs=True)

        self.logger.info("Loading config file from {}".format(config_file_path))
        self.config = get_config(config_file_path)

        self.exclusion_criteria = {k: v for k, v in get_ante_config().items() if v["type"] == "exclusion_criteria"}

        # load rating bool
        with open(self.config.resource_files.rating_bool, "rb") as f:
            self.rating_bool = pd.read_csv(f, index_col=0)

        # to access membership functions of Antecedents, we have to get original XAIRecommenderInput from
        # config file
        # with open(self.config.resource_files.antecedents, "rb") as f:
        self.criteria = np.load(self.config.resource_files.antecedents, allow_pickle=True).item()

        super().__init__(rules)

    def print_rules(self):
        """
        Prints existing rules of XAIR. Rules with only a "NOOP" triggering consequent are ignored.
        """
        total_rules = set()
        for rule in self.rules:
            for c in rule.consequent:
                c = c[0] if isinstance(c, list) else c
                if "NOOP" not in c.term.full_label:
                    total_rules.add("{} -> {}".format(rule.antecedent, rule.consequent))
        s = "\n".join(total_rules)
        print(s)

        # just for me :)
        with open(self.config.resource_files.cur_rules_file, "w") as f:
            f.write(s)

    def get_memberships_of_inputs(self, input_dict):
        """
        Determine fuzzy memberships for crisp inputs

        :param input_dict: dict with input name as key and exact input value as value
        :return dict with input name as key and dict of fuzzy membership values as value
        """

        # if boolean criteria/ exclusion criteria or non processable values are given, remove them
        # if any([True for val in input_dict.values() if isinstance(val, bool) or val in self.config.criteria.disable_processing]):
        #   _, inputs = self.__prepare_inputs(input_dict)

        inputs = {k: v for k, v in input_dict.items() if
                  k not in self.exclusion_criteria and k in self.criteria.keys()}

        def __get_all_memberships(universe, memberships, val):
            rating = [r for r in self.config.ratings if len(r) == len(memberships)][0]

            mems = {}
            if isinstance(val, str) and val in rating:
                # full membership for already fuzzy value
                for r in rating:
                    mems[r] = 1.0 if r == val else 0.0
            else:
                for idx, m in enumerate(memberships):
                    mems[rating[idx]] = np.around(fuzz.interp_membership(universe, m, val), 3)
            return mems

        input_memberships = {}
        for input_name, value in inputs.items():
            universe = np.array(self.criteria[input_name].variable.universe)
            mem_func = list(self.criteria[input_name].mem_funcs.values())
            memberships = __get_all_memberships(universe, mem_func, value)
            input_memberships[input_name] = memberships
            # print("{}: \n  {}".format(input_name, memberships))
        return input_memberships


class XAIRecommenderSimulation(ctrl.ControlSystemSimulation):
    """
    Wrapper frunction for scikit-fuzzy ControlSystemSimulation
    Besides dict of outputs additionally contains
        - remaining XAI methods (not excluded) and exclusion criteria
        - active rules
    """

    def __init__(self, config_file_path):
        # get logger
        self.logger = get_logger(__name__, activate_console_logs=True)
        self.active_rules = None

        self.config = get_config(config_file_path)

        self.exclusion_reasons = None

        # create schema for validation of input types
        self.input_validator = self.__create_input_validator()

        # load rules and create Control System
        self.logger.info("Loading rules from '{}'...".format(self.config.resource_files.rules))
        try:
            with open(self.config.resource_files.consequent_config) as f:
                consequents = json.load(f)
                # name, not label
                self.remaining_methods = consequents.keys()
            with open(self.config.resource_files.rules, "rb") as f:
                rules = pickle.load(f)
        except IOError as ioe:
            self.logger.error("Error in loading resource files")
            self.logger.error(ioe)
            raise ioe

        super().__init__(XAIRecommenderControlSystem(rules, config_file_path))

    def __prepare_inputs(self, input_dict):
        """
            Prepares inputs for later decisions.
            Adds foi_available antecedent to input dict, depending on given FOI
            Fuzzy and boolean values, which are used for rules within inference, are transformed to crisp values.

            @param input_dict:
                dict with input name as key and input value as value

            @returns prepared dicts for boolean and other values
        """

        def __validate_inputs(inputs):
            """
                Remove foi specific criteria if no FOI available and validate input with input_validator
            """
            validated_inputs = inputs.copy()
            foi_specific = [f for f in validated_inputs.keys() if "_foi" in f]
            # foi_specific = ["corr_foi", "discr_foi"]

            # remove foi specific criteria if no FOI available
            if len(inputs["foi"]) == 0:
                validated_inputs["foi_available"] = False
                # set foi specific one to general one (will be ignored due to rule prerequisite of "foi_available"
                for f in foi_specific:
                    validated_inputs[f] = inputs[f.replace("_foi", "")]
            else:
                assert len(foi_specific) == len([True for f in foi_specific if inputs[f] is not None]), \
                    "If list of FOI is given ({}), FOI-specific inputs must not be None".format(inputs["foi"])
                validated_inputs["foi_available"] = True

            if not self.input_validator.validate(input_dict):
                raise ValueError(f"Inputs not valid:\n{self.input_validator._errors}")
            return validated_inputs

        def __convert_fuzzy_input(input_name, input_value):
            """
                Transform fuzzy values to maximum of fuzzy membership function.

                @param input_name: Name of input value (Antecedent)
                @param input_value: Fuzzy input value

                @returns Crisp input value
            """

            import statistics

            try:
                if isinstance(input_value, bool):
                    input_value = str(input_value)
                ante = get_ante_config()[input_name]
                mem_f = ante["mem_funcs"][ante["rating"].index(input_value)]
                # get index of universe array where membership is max
                # median, since mem funcs triangular or trapez
                max_mem = ante["universe"].index(round(statistics.median(mem_f)))
            except KeyError as e:
                self.logger.warning(e)
                try:
                    float_val = float(input_value)
                    # if accidentally float, return upscaled float value
                    return float_val * 10
                except ValueError:
                    self.logger.error(
                        "No membership can be determined for input '{}' with fuzzy rating {}".format(input_name,
                                                                                                     input_value))
                    raise ValueError(
                        "No membership can be determined for input '{}' is {}".format(input_name, input_value))
            return max_mem

        inputs = __validate_inputs(input_dict)

        # if not fuzzy, upscale float values to range of 10
        # all inputs regarding data
        # upscale correlation and discretization to a universe of 10
        def upscale(feat):
            try:
                return True if get_ante_config()[feat]["frontend"]["max"] == 1 else False
            except KeyError:
                return False

        [inputs.update({i: input_dict[i] * 10}) for i in
         [k for k, v in input_dict.items() if upscale(k)]]  # isinstance(v, float)]]

        # registered antecedents
        antes = [k for k, v in get_ante_config().items() if v["type"] != "other" and v["type"] != "exclusion_criteria"]

        # if string input: Transform fuzzy values to maximum of fuzzy membership function.
        # all other values not in exclusion_criteria or keep_inputs
        convert_vals = [k for k, v in get_ante_config().items()
                        if k in inputs.keys() and not isinstance(inputs[k], (int, float))
                        and k in antes]

        try:
            [inputs.update({f: __convert_fuzzy_input(f, inputs[f])}) for f in convert_vals]
            # sort values according to type (boolean and processed by fuzzy inference)
            # dismiss keep_inputs variables (used for specific error messages)
            bool_dict = {}
            range_dict = {}
            for l, v in inputs.items():
                if l in self.ctrl.exclusion_criteria:
                    bool_dict[l] = v
                elif l in antes:
                    range_dict[l] = v
                else:
                    pass

            # add value for init to make initial rule (value does not matter)
            range_dict["init"] = 0

            return bool_dict, range_dict
        except Exception as e:
            self.logger.error("Error during fuzzy input conversion")
            self.logger.error(e)

    def __remove_unusable_alternatives(self):
        """
            Remove alternatives which execution is not possible (criteria: see rating bool CSV)

            @returns List of possible alternatives
            @returns Dict with eliminated alternative as key and kick-out-criterion as value
        """
        assert len(self.ctrl.rating_bool.index) == len(
            self.input_bool), "Number of inputs does not match number of rows in rating DataFrame"

        # get name (not label) of all methods

        remaining_methods = list(self.ctrl.rating_bool.columns.values)
        exclusion_reasons = {}

        for method in self.ctrl.rating_bool.columns.values:
            ratings = self.ctrl.rating_bool[method].to_dict()
            for n in ratings.keys():
                # if self.input_bool[n] > ratings[n]:
                # print("Criterion '{}': input: {}, rating: {}".format(n, int(self.input_bool[n]), ratings[n]))
                if n in self.input_bool and self.input_bool[n] < ratings[n]:
                    # if conditional, check whether condition is met
                    if "condition" in get_ante_config()[n]:
                        if self.input_bool[get_ante_config()[n]["condition"]["crit"]] != \
                                get_ante_config()[n]["condition"]["value"]:
                            continue

                    self.logger.debug("Criterion '{}' kicks out alternative '{}'".format(n, method))
                    exclusion_reasons.setdefault(method, []).append(n)
                    if method in remaining_methods: remaining_methods.remove(method)

        return remaining_methods, exclusion_reasons

    def inputs(self, input_dict, return_inputs=False):
        """
            Validates and sets input_fuzzy and inputs_bool from raw system input
            @param input_dict: Dict with plain input variables
        """

        # restart simulation every time
        if self.cache:
            self._reset_simulation()

        try:
            # if input valid, set input_params
            self.input_bool, input_fuzzy = self.__prepare_inputs(input_dict)

            # sets input
            super().inputs(input_fuzzy)

            if return_inputs:
                return self.input_bool, input_fuzzy
            return None;

        except ValueError:
            raise ValueError(f"Inputs are not valid: {self.input_validator.errors}")

    def __create_input_validator(self):
        """
            Create validator according to data types of antecedents in antecedent config
            @return: validator
        """
        schema = {}
        # {a: v["dtypes"]["crisp"] for a,v in c.items() if "dtypes" in v}
        # for key, crisp_val in self.config.input_dtypes.crisp.__dict__.items():

        for key, crisp_val in {a: v["dtypes"]["crisp"] for a, v in get_ante_config().items() if "dtypes" in v}.items():
            if crisp_val == "bool":
                # boolean are all the same
                schema[key] = {"type": "boolean"}
            elif crisp_val == "list":
                schema[key] = {"type": "list", "schema": {"type": "string"}}
            else:
                if crisp_val == "str":
                    # for input via web gui allow numbers
                    schema[key] = {
                        "anyof": [
                            {"type": "float", "anyof": [{"min": 0., "max": 1.}, {"min": 0., "max": 10.}]},
                            {"type": "string", "allowed": ["VL", "L", "M", "H", "VH"]}
                        ]}
                else:
                    if "foi" in key:
                        # multiple definitions of nullable necessary
                        schema[key] = {"nullable": True,
                                       "anyof": [
                                           {"type": "float", "nullable": True, "allof": [{"min": 0., "max": 1.}]},
                                           {"type": "string", "nullable": True}
                                       ]}
                    else:
                        schema[key] = {
                            "anyof": [{"type": "string"}, {"type": "float", "allof": [{"min": 0., "max": 1.}]}]}
        self.logger.info(f"Created input validation schema:\n {schema}")

        return Validator(schema, allow_unknown=True, require_all=True)

    def compute(self):
        """
            Compute rule activation and result.
            Set final recommendation (output_reommendation) and rules activated (active_rules)
        """
        # call original compute method in self.output
        super().compute()

        # TODO process exclusion_reasons
        self.remaining_methods, self.exclusion_reasons = self.__remove_unusable_alternatives()

        output_tmp = [(name, np.around(val, decimals=3)) for name, val in self.output.items() if
                      name in self.remaining_methods]
        output_tmp = sorted(output_tmp, key=lambda x: x[1], reverse=True)

        # don't modify self.output, since it's reused when calculating other outputs
        self.output_recommendation = output_tmp

        # trigger set active rules
        self.active_rules = self.get_active_rules()

    def get_active_rules(self, by_output=None):
        """
            Check which rules were activated during computation

            @returns HTML code as string to display in frontend app
            @returns string of printable rules
        """

        def is_activated(inputs, rule):
            """
                Check whether rule got activated

                @param inputs:
                    List of string representations of antecedents
                @param rule:
                    Rule or Term or TermAggregation

                @returns True if conditions for rule are fulfilled, False otherwise
            """

            if isinstance(rule, fuzz.control.Rule):
                # if it's a rule, get proposition term
                a = rule.antecedent
            else:
                # otherwise take term (if recursive call)
                a = rule

            if isinstance(a, fuzz.control.term.Term):
                # if assumption is simple term: check if inputs contain term value
                return True if str(a) in inputs else False
            else:
                # if assumption is aggregated term: check activation of single terms
                assert isinstance(a, fuzz.control.term.TermAggregate)
                t1 = is_activated(inputs, a.term1)
                t2 = is_activated(inputs, a.term2)

                if a.kind == "and":
                    return (t1 and t2)
                else:
                    return (t1 or t2)

        def get_html(term, idx):
            """
                @returns String of HTML representation of single term
            """

            label = get_ante_config()[term.parent.label][
                'label'] if idx == 0 else f"+ {get_ante_config()[term.parent.label]['label']}"
            # some criteria should not be displayed in frontend and do not contain config for that
            # e.g. "foi_available". Skip!
            try:
                if "corr" in term.parent.label or "dur_call" in term.parent.label:
                    css_class = "L" if term.label == "H" else "H"
                else:
                    css_class = term.label
                return f"<div><span class='param'>{label}: </span>" \
                       f"<span class='rating {css_class}'>{get_ante_config()[term.parent.label]['frontend']['rating'][str(term.label)]}</span></div>"
            except KeyError as e:
                self.logger.debug(f"Criteria '{term.parent.label}' not displayed in frontend.")
                return ""

        # get fuzzy values
        triggered = []
        rules = []
        printable_rules = []

        # bring inputs into format of antecedents (string)
        for idx, (key, m) in enumerate(self.ctrl.get_memberships_of_inputs(self.input._get_inputs()).items()):
            for mem_idx, value in m.items():
                if value > 0:
                    triggered.append("{}[{}]".format(key, mem_idx))

        # search for specific output if given
        remaining_alts = [by_output] if by_output is not None else self.remaining_methods

        # iterate over all rules
        for r in self.ctrl.rules:
            # check if activated and not init rule
            if is_activated(triggered, r) and "init" not in str(r.antecedent):
                # avoid duplicates in list of rules
                already_added = False
                # iterate over consequents of activated rule
                for c in r.consequent:
                    # continue, if output is the demanded output
                    if c.term.full_label.split("[")[0] in remaining_alts and not already_added:
                        # for a in r.antecedent_terms:
                        # don't print foi_available label
                        rules.append(([get_html(a, idx) for idx, a in enumerate(
                            [t for t in r.antecedent_terms if t.parent.label != "foi_available"])],
                                      r.consequent))
                        # TODO split rules here or show as string??
                        printable_rules.append("{} -> {}".format(str(r.antecedent), r.consequent))
                        # rules.append((str(r.antecedent), r.consequent))
                        already_added = True

        self.logger.debug("Activated rules: ", [r for r in rules])

        df_index = set(sorted([str(r[0])[2:-2] for r in rules], key=lambda x: str(x[0])))
        # create dataframe to return in html
        df = pd.DataFrame(columns=[c for c in remaining_alts], index=df_index)

        # fill dataframe
        for r in rules:
            for c in r[1]:
                # rating equals column name
                # can be weighted as well
                c = c[0] if isinstance(c, list) else c
                if c.term.parent.label in remaining_alts:
                    if c.weight < 1.0:
                        # if weight mention it
                        df.at[str(r[0])[
                              2:-2], c.term.parent.label] = f"<span class='rating {c.term.label}'>rather {RATING_METHODS[c.term.label]}</span>"  # ({c.weight * 100}%)" --> without percentage
                    else:
                        df.at[str(r[0])[
                              2:-2], c.term.parent.label] = f"<span class='rating {c.term.label}'>{RATING_METHODS[c.term.label]}</span>"

        df = df.fillna("")
        # generate html string to return to frontend
        html = df.to_html(classes=["responsive rulesTable"])

        # write html to file - just for me :)
        # text_file = open("./resources/testTable.html", "w")
        # text_file.write(html)
        # text_file.close()

        # [print(r) for r in printable_rules]
        return html, printable_rules

    def plot_output_membership(self, output=[], save=False):
        """
            Plot output membership of given output variables or all outputs
        """
        for consequent in self.ctrl.consequents:
            print(consequent.label)
            if consequent.label.lower() != "noop" and consequent.label in output:
                calc = CrispValueCalculator(consequent, self)

                # upsampled universe, ouput membership function, mem funcs for single terms
                ups_universe, output_mf, term_mfs = calc.find_memberships()

                plot_membership(consequent.label, ups_universe, output_mf, save)
                consequent.output[self] = calc.defuzz()
                print("Output using centroid: ", consequent.output[self])
