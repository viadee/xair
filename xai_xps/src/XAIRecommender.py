import json
import numpy as np
import os
import pickle
import skfuzzy as fuzz
import sys
from Utils import get_logger, get_config, CONFIG_FILE, get_ante_config
from XAIRInitializer import XAIRInitializer
from XAIRecommenderVariables import XAIRecommenderSimulation, XAIRecommenderControlSystem
from types import SimpleNamespace

sys.path.append("./../")


class XAIRecommender:

    def __init__(self, reload=False, config_file_path=CONFIG_FILE, verbose=False):
        """
        Initialize XAIRecommender

        @param reload: Whether to reload system variables (antecedents, consequents) and rules. Default: False
        @param config_file_path: custom config file path
        @param verbose: Whether to print additional statements about progress. Default: False
        """

        # get logger
        self.logger = get_logger(__name__, activate_console_logs=verbose)
        self.verbose = verbose

        try:
            self.logger.info("Loading config file from {}".format(config_file_path))

            # reload if custom config is used
            if config_file_path != CONFIG_FILE:
                reload = True

            self.ante_config = get_ante_config(reload=reload)
            with open(get_config(config_file_path).resource_files.consequent_config) as f:
                self.conse_config = json.load(f)
        except:
            # if no json file of ante_config is available, generate from antecedent_config.py
            self.logger.info("No JSON of antecedent config available. Creating default one.")

        XAIRInitializer(verbose=verbose).initialize(reload=reload)

        try:
            self.rec_sim = XAIRecommenderSimulation(config_file_path)
            self.logger.debug("Antecedents:   {}".format([a.label for a in self.rec_sim.ctrl.antecedents]))
            self.logger.debug("Consequents:   {}".format([a.label for a in self.rec_sim.ctrl.consequents]))
        except IOError as ioe:
            self.logger.error(ioe)
            raise ioe

    def make_recommendation(self, inputs: dict, return_inputs=False):
        """
            Compute all rule activations
            Then remove all XAI methods that cannot be applied due to unmet requirements.

            @param inputs: Dict of input values
            @param return_inputs: Whether or not to return original input values (used for web application)

            @returns recommendation result, original inputs (optional)
        """

        try:
            self.logger.info("Make recommendation...")
            # insert into recommender
            inputs = self.rec_sim.inputs(inputs, return_inputs)
            # Crunch the numbers
            self.rec_sim.compute()

            self.logger.info("--" * 50)
            self.logger.info("--- RECOMMENDATION:   {} --- ".format(self.rec_sim.output_recommendation))
            self.logger.info("--" * 50)

            # get name and label
            result = []
            for rec in self.rec_sim.output_recommendation:
                name = [k for k, v in self.conse_config.items() if v["label"] == rec[0]][0]
                result.append({"name": name, "label": rec[0], "rating": rec[1]})

            # fuzzy terms of inputs are required for frontend application to show the user
            if return_inputs:

                # gets all memberships > 1 and joins them to string
                mems_str = {k: "/".join([self.ante_config[k]['frontend']['rating'][midx] for midx, m in v.items() if
                                         "frontend" in self.ante_config[k] and m > 0]) for k, v in
                            self.rec_sim.ctrl.get_memberships_of_inputs(inputs[1]).items()}

                if not inputs[1]["foi_available"]:
                    for key in list(mems_str.keys()):
                        if "foi" in key:
                            del mems_str[key]

                return result, {"bool": inputs[0], "fuzzy": mems_str}
            return result


        except ValueError as e:
            self.logger.error("Error in computing result with input parameters: {}".format(inputs))
            return e, 400

    def plot_output_membership(self, output_list=[], save=False):
        """
            Convenience method for getting memberships of inputs from XAIRecommenderSimulation
        """
        self.rec_sim.plot_output_membership(output_list, save)

    def get_memberships_of_inputs(self, inputs):
        """
            Convenience method for getting memberships of inputs from XAIRecommenderSimulation
        """
        self.rec_sim.ctrl.get_memberships_of_inputs(inputs)

    def get_active_rules(self, by_output=None):
        """
            Convenience method for getting active rules from XAIRecommenderSimulation
        """
        if by_output is None:
            return self.rec_sim.active_rules
        return self.rec_sim.get_active_rules(by_output=by_output)

    def print_rules(self):
        """
            Convenience method for printing rules from XAIRecommenderControl
        """
        self.rec_sim.ctrl.print_rules()

    def get_method_information(self):
        """
        Convenience method for getting active rules from XAIRecommenderSimulation

        @returns
            - List of available methods
            - Dict with method as key and exclusion reasons as value
        """
        return self.rec_sim.remaining_methods, self.rec_sim.exclusion_reasons
