import json
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import skfuzzy as fuzz
import sys
from cerberus import Validator
from types import SimpleNamespace

CONFIG_FILE = "./resources/config/config.json"
ANTE_CONFIG_FILE = "./resources/config/antecedent_config.json"
CONFIG_VALIDATION = "./../resources/validation/config_schema.json"

__config = None
__ante_config = None


def get_config(config_file=CONFIG_FILE, reload=False):
    """
        @param config_file: config file path (default: "./resources/config/config.json")
        @param reload: whether or not to reload config file (default: False)

        @returns config as namespace
    """
    global __config
    config_file = config_file if config_file is not None else CONFIG_FILE
    if __config is None or config_file != CONFIG_FILE or reload:
        with open(config_file) as f:
            __config = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    return __config


def get_ante_config(config_file=ANTE_CONFIG_FILE, reload=False):
    """
        Loads antecedent config. If no config file is available yet,
        initial config file gets recreated from python config file.

        @param config_file: antecedent config file path (default: "./resources/config/antecedent_config.json")
        @param reload: whether or not to reload config file (default: False)

        @returns config as namespace
    """
    global __ante_config
    config_file = config_file if config_file is not None else ANTE_CONFIG_FILE
    if __ante_config is None or config_file != ANTE_CONFIG_FILE or reload:
        try:
            with open(config_file) as f:
                __ante_config = json.load(f)
        except FileNotFoundError:
            # if file is deleted, generate new one from convenience file (default antecedents!!)
            from resources.config.antecedent_config import antecedents as ac
            # if no json file of ante_config is available, generate from antecedent_config.py
            with open(config_file, 'w') as fp:
                json.dump(ac, fp)
            __ante_config = ac
    return __ante_config


def plot_membership(var_name, x, mfx, save=False):
    """
        Plot membership function.
        Defuzzification of a membership function, returning a defuzzified value of the function at x, using various 
        defuzzification methods (COG,MOM,SOM,LOM)

        @param var_name: Name of variable
        @param x:  Independent variable (1d array or iterable, length N)
        @param mfx: Fuzzy membership function (1d array of iterable, length N)
        
    """
    # Defuzzify this membership function five ways
    print("--- ", var_name, ", x: ", x, " mfx: ", mfx)
    defuzz_centroid = fuzz.defuzz(x, mfx, 'centroid')  # Same as skfuzzy.centroid
    # defuzz_bisector = fuzz.defuzz(x, mfx, 'bisector')
    defuzz_mom = fuzz.defuzz(x, mfx, 'mom')
    defuzz_som = fuzz.defuzz(x, mfx, 'som')
    defuzz_lom = fuzz.defuzz(x, mfx, 'lom')

    # Collect info for vertical lines
    # labels = ['centroid', 'bisector', 'mean of maximum', 'min of maximum', 'max of maximum']
    labels = ['COG', 'Mean of Maximum', 'Min of Maximum', 'Max of Maximum']
    xvals = [defuzz_centroid,
             # defuzz_bisector,
             defuzz_mom,
             defuzz_som,
             defuzz_lom]
    colors = ["b", "g", "r", "y", "m"]
    ymax = [fuzz.interp_membership(x, mfx, i) for i in xvals]

    # Display and compare defuzzification results against membership function
    plt.figure(figsize=(8, 4))

    plt.plot(x, mfx, 'k')
    for xv, y, label, color in zip(xvals, ymax, labels, colors):
        plt.vlines(xv, 0, y, label=label, color=color)
    plt.ylabel('Zugehörigkeitswert')
    plt.xlabel('Diskursuniversum ({})'.format(var_name))
    #plt.ylabel('Fuzzy membership')
    #plt.xlabel('Universe variable ({})'.format(var_name))
    #plt.ylim(-0.1, 1.1)
    plt.legend(loc=2)

    if save:
        plt.savefig(f"./../defuzz_{var_name}.png",dpi=300)

    plt.show()


def get_logger(name, activate_console_logs=True, log_file=get_config().resource_files.log_file, log_level=logging.INFO):
    '''
    Returns logger which logs to console on a specified level

    @param activate_console_logs: If true, logs are also printed in the console. Default: True
    @param log_file: File to write logs to. Default: config.resource_files.log_file
    @param log_level: Level of which to log events

    @returns Logger
    '''
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger(name)

    fileHandler = logging.FileHandler(log_file)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(log_level)
    rootLogger.addHandler(fileHandler)

    if activate_console_logs:
        consoleHandler = logging.StreamHandler()  # (sys.stdout)
        consoleHandler.setFormatter(logFormatter)
        consoleHandler.setLevel(log_level)
        rootLogger.addHandler(consoleHandler)
        rootLogger.setLevel(logging.DEBUG)

    return rootLogger


############################ KNOWLEDGE AQUISITION ############################

def create_exclusion_criteria(name, label, help_txt, section, method_rating):
    """
        Adds rating of criteria to dataframe and returns antecedent configuration
         to be added to ante_config
        Attention: Formulate Boolean criteria, that application of the method is
        possible when input variable >= Rating of method in dataframe

        @param name: name of criterion
        @param label: label of criterion
        @param help_txt: help text
        @param section: section to display criterion in
        @param method_rating: Rating for every available XAI-method (1d array, length of available methods)
    """
    excl_criteria_df = pd.read_csv(get_config().resource_files.rating_bool, index_col=[0])
    assert len(method_rating) == len(
        excl_criteria_df.columns), f"Length of given method ratings ({len(method_rating)}) doesn't match length of " \
                                   f"rating dataframe ({len(excl_criteria_df.columns)})"

    # add to boolean rating dataframe
    excl_criteria_df.loc[name] = method_rating
    # save dataframe back
    excl_criteria_df.to_csv(get_config().resource_files.rating_bool)

    return {
        "label": label,
        "type": "exclusion_criteria",
        "dtypes": {
            "fuzzy": "bool",
            "crisp": "bool"
        },
        "frontend": {
            "type": "checkbox",
            "section": section,
            "help": help_txt,
            "initialValue": True,
            "rating": "bool"
        }
    }


def add_method(name, label, visualization, exclusion_ratings, fuzzy_ratings):
    """
        Add methods to backend application of XAIR

        @param name: name of method
        @param label: label to be displayed
        @param visualization: 1 if visualization method, 0 otherwise
        @param exclusion_ratings: 1d array of method rating regarding exclusion criteria (length: number of exclusion criteria)
        @param fuzzy_ratings: 1d array of method rating regarding fuzzy criteria (length: number of all possible fuzzy criteria levels)

    """
    # add exclusion criteria rating
    excl_criteria_df = pd.read_csv(get_config().resource_files.rating_bool, index_col=[0])
    excl_criteria_df[label] = exclusion_ratings
    excl_criteria_df.to_csv(get_config().resource_files.rating_bool)

    # add fuzzy rating
    fuzzy_df = pd.read_csv(get_config().resource_files.rating_fuzzy, index_col=[0, 1])
    fuzzy_df[label] = fuzzy_ratings
    fuzzy_df.to_csv(get_config().resource_files.rating_fuzzy)

    # add to alternatives in config
    with open(get_config().resource_files.consequent_config) as f:
        c = json.load(f)
        c[name] = {'label': label,
                                   'visualization': visualization}
    with open(get_config().resource_files.consequent_config, 'w') as fp:
        json.dump(c, fp)

    return True


def create_criteria(label,
                    help_txt,
                    crit_type,
                    standalone_impact,
                    disable_processing,
                    section,
                    input_type,
                    rating,
                    universe,
                    mem_funcs,
                    dtypes,
                    init_value=None,
                    max_value=None,
                    min_value=None
                    ):
    """
        Create criterion JSON format from input values

        @retuns criterion JSON structure
    """

    crit = {"label": label,
            "universe": universe,
            "mem_funcs": mem_funcs,
            "rating": list(rating.keys()),
            "type": crit_type,
            "dtypes": dtypes,
            "rules": {
                "standalone_impact": standalone_impact,
                "disable_processing": disable_processing
            },
            "frontend": {
                "type": input_type,
                "section": section,
                "help": help_txt,
                "rating": rating
            }}
    if input_type not in ["list", "text"]:
        assert init_value is not None, "Initial value for frontend must be given for number/range inputs."
        assert max_value is not None, "Max value for frontend must be given for number/range inputs."
        assert min_value is not None, f"Min value for frontend must be given for number/range inputs. ({min_value})"

        crit["frontend"]["initialValue"] = init_value
        crit["frontend"]["max"] = max_value
        crit["frontend"]["min"] = min_value
        crit["frontend"]["range_min"] = list(rating.values())[0]
        crit["frontend"]["range_max"] = list(rating.values())[-1]

    return crit
