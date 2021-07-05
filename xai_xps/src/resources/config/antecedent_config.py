### Convenience file for good readability ###


from Utils import get_config

config = get_config()

# load universes
u_10 = config.fuzzy.universes.u_10
u_10_neg = config.fuzzy.universes.u_10_neg
u_bool = config.fuzzy.universes.u_bool

# load membership function shapes
m_trap_5_10 = config.fuzzy.mem_funcs.trap.u10_5
m_bool = config.fuzzy.mem_funcs.bool
m_tri_3_10 = config.fuzzy.mem_funcs.tri.u10_3

# load ratings
rating_5 = [r for r in config.ratings if len(r) == 5][0]
rating_3 = [r for r in config.ratings if len(r) == 3][0]
rating_bool = [r for r in config.ratings if len(r) == 2][0]

# parameter type

EXCLUSION_CRIT = "exclusion_criteria"
RATING_CRIT = "rating_criteria"
OTHER = "other"
crit_types = [EXCLUSION_CRIT,RATING_CRIT,OTHER]

SEC_MODEL = "model"
SEC_DATA = "data"
SEC_PREFS = "preference"

sections = [SEC_MODEL, SEC_DATA, SEC_PREFS]

INPUT_RANGE = "range"
INPUT_CHECKBOX = "checkbox"
INPUT_TEXT = "text"
INPUT_LIST = "list"
INPUT_NUMBER = "number"
input_types = [INPUT_RANGE, INPUT_CHECKBOX, INPUT_TEXT, INPUT_LIST, INPUT_NUMBER]

# frontend ratings german
GERMAN_RATING_METHODS = {
    "VL": "sehr schlecht",
    "L": "schlecht",
    "M": "mittelmäßig",
    "H": "gut",
    "VH": "sehr gut"
}
GERMAN_RATING_BOOL = {
    "False": "nein",
    "True": "ja"
}
GERMAN_RATING_STRONGNESS = {
    "VL": "sehr gering",
    "L": "gering",
    "M": "mittelstark",
    "H": "stark",
    "VH": "sehr stark",
}

GERMAN_RATING_BAD = {
    "L": "schlecht",
    "M": "mittelmäßig",
    "H": "gut"
}

GERMAN_RATING_DURATION = {
    "L": "kurz",
    "M": "mittel",
    "H": "lang"
}
GERMAN_RATING_NUMBER = {
    "L": "wenig",
    "M": "mittel",
    "H": "viel"
}

german_ratings = {"bool": GERMAN_RATING_BOOL,
                  "strongness": GERMAN_RATING_STRONGNESS,
                  "good": GERMAN_RATING_BAD,
                  "duration": GERMAN_RATING_DURATION,
                  "number": GERMAN_RATING_NUMBER}

# english

RATING_METHODS = {
    "VL": "very bad",
    "L": "bad",
    "M": "medium",
    "H": "good",
    "VH": "very good"
}

RATING_BOOL = {
    "False": "no",
    "True": "yes"
}
RATING_STRONGNESS = {
    "VL": "very weak",
    "L": "weak",
    "M": "medium strong",
    "H": "strong",
    "VH": "very strong",
}

RATING_BAD = {
    "L": "bad",
    "M": "medium",
    "H": "good"
}

RATING_DURATION = {
    "L": "fast",
    "M": "medium",
    "H": "long"
}
RATING_NUMBER = {
    "L": "few",
    "M": "medium",
    "H": "many"
}

RATING_AMOUNT = {
    "L": "low",
    "M": "medium",
    "H": "high"
}

english_ratings = {"bool": RATING_BOOL,
                   "strongness": RATING_STRONGNESS,
                   "good": RATING_BAD,
                   "duration": RATING_DURATION,
                   "number": RATING_NUMBER,
                   "amount": RATING_AMOUNT}

## ORDER OF ANTECEDENTS DEFINES THE ORDER IN INPUT PAGE OF FRONTEND!
antecedents = {
    # for frontend only
    "model_name": {
        "label": "Model name",
        "type": OTHER,
        "rules": {
            "standalone_impact": False,
            "disable_processing": True
        },
        "frontend": {
            "type": INPUT_TEXT,
            "section": SEC_MODEL,
            "help": "Name of your model (only relevant for you to distinguish your recommendations)",
            "initialValue": ""
        }
    },
    # exclusion criteria (only for frontend)
    "model": {
        "label": "Model available",
        "type": EXCLUSION_CRIT,
        "dtypes": {
            "fuzzy": "bool",
            "crisp": "bool"
        },
        "frontend": {
            "type": INPUT_CHECKBOX,
            "section": SEC_MODEL,
            "help": "Is the ML Model available or only the prediction function?",
            "initialValue": True,
            "rating": RATING_BOOL
        }
    },
    "classif": {
        "label": "Classification task",
        "type": EXCLUSION_CRIT,
        "dtypes": {
            "fuzzy": "bool",
            "crisp": "bool"
        },
        "frontend": {
            "type": INPUT_CHECKBOX,
            "section": SEC_MODEL,
            "help": "Does the model solve a classification task?",
            "initialValue": True,
            "rating": RATING_BOOL
        }
    },
    # exclusion criteria (only for frontend)
    "predict_proba": {
        "label": "Class probabilities",
        "type": EXCLUSION_CRIT,
        "dtypes": {
            "fuzzy": "bool",
            "crisp": "bool"
        },
        "condition": {
            "crit": "classif",
            "value": True
        },
        "frontend": {
            "type": INPUT_CHECKBOX,
            "section": SEC_MODEL,
            "help": "Are the calibrated probabilities of the classification according to each class returned by the prediction function? (This will only be taken into consideration if it's a classification task)",
            "initialValue": True,
            "rating": RATING_BOOL,
            "conditionalRender": "classif"
        }
    },
    "prep_ops": {
        "label": "Preprocessing Operations available",
        "type": EXCLUSION_CRIT,
        "dtypes": {
            "fuzzy": "bool",
            "crisp": "bool"
        },
        "frontend": {
            "type": INPUT_CHECKBOX,
            "section": SEC_MODEL,
            "help": "Are the preprocessing operations (e.g. label encoding, numerical transformations) available and reversible?",
            "initialValue": True,
            "rating": RATING_BOOL
        }
    },
    "dur_call": {
        "label": "Duration of Model Call",
        "universe": u_10,
        "mem_funcs": m_tri_3_10,
        "rating": rating_3,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "str",
            "crisp": "str"
        },
        "rules": {
            "standalone_impact": False,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_RANGE,
            "section": SEC_MODEL,
            "range_min": "short",
            "range_max": "long",
            "help": "How long does it take to access the model or the prediction function? (Important for XAI-method performance)",
            "initialValue": 0,
            "min": 0,
            "max": 10,
            "rating": RATING_DURATION
        }
    },

    # data stuff

    "corr": {
        "label": "Correlation",
        "universe": u_10,
        "mem_funcs": m_trap_5_10,
        "rating": rating_5,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "str",
            "crisp": "float"
        },
        "rules": {
            "standalone_impact": True,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_NUMBER,
            "section": SEC_DATA,
            "range_min": "negligible",
            "range_max": "high",
            "help": "How high/strong is the correlation of the dataset (considering the number of correlating features and the strength of ALL the correlations)?",
            "initialValue": 0,
            "min": 0,
            "max": 1,
            "rating": RATING_STRONGNESS
        }
    },

    "discr": {
        "label": "Discretizability",
        "universe": u_10_neg,
        "mem_funcs": [[-10, -10, 0, 5], [0, 5, 10], [5, 9, 10, 10]],
        "rating": rating_3,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "str",
            "crisp": "float"
        },
        "rules": {
            "standalone_impact": True,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_NUMBER,
            "section": SEC_DATA,
            "range_min": "poor",
            "range_max": "good",
            "help": "How well discretizable are the numerical features? Discretizability is given if the data points of a feature distribution can be divided into intervals of equal size (equal-width binning) with a similar number of data points, or into bins with equal frequency (e.g. deciles/quartiles) with a similar width.",
            "initialValue": 0,
            "min": 0,
            "max": 1,
            "rating": RATING_BAD
        }
    },
    "num_feat": {
        "label": "Number of Features",
        "universe": u_10,
        "mem_funcs": m_tri_3_10,
        "rating": rating_3,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "str",
            "crisp": "str"
        },
        "rules": {
            "standalone_impact": False,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_RANGE,
            "section": SEC_DATA,
            "range_min": "few",
            "range_max": "many",
            "help": "How many features does the dataset have (including One-Hot encoded)? (Important for XAI-method performance)",
            "initialValue": 0,
            "min": 0,
            "max": 10,
            "rating": RATING_NUMBER
        }
    },

    "foi": {
        "label": "Features of Interest (FOI)",
        "type": OTHER,
        "dtypes": {
            "fuzzy": "list",
            "crisp": "list"
        },
        "rules": {
            "standalone_impact": False,
            "disable_processing": True
        },
        "frontend": {
            "type": INPUT_LIST,
            "section": SEC_DATA,
            "help": "Which features are likely to offer the potential for discrimination and therefore need special attention (for example 'gender', 'race', 'age')? Please insert them, separated by a ','.",
            "initialValue": ""
        }
    },
    "corr_foi": {
        "label": "Correlation FOI",
        "universe": u_10,
        "mem_funcs": m_trap_5_10,
        "rating": rating_5,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "str",
            "crisp": "float"
        },
        "rules": {
            "standalone_impact": False,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_NUMBER,
            "section": SEC_DATA,
            "range_min": "negligible",
            "range_max": "high",
            "help": "How high/strong is the correlation of the features of interest (taking into account the number and strength of correlations with ALL input features)? This will not be taken into consideration if no Features of Interests are given!",
            "initialValue": 0,
            "min": 0,
            "max": 1,
            "rating": RATING_STRONGNESS,
            "conditionalRender": "foi"
        }
    },
    "discr_foi": {
        "label": "Discretizability FOI",
        "universe": u_10_neg,
        "mem_funcs": [[-10, -10, 0, 5], [0, 5, 10], [5, 9, 10, 10]],
        "rating": rating_3,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "str",
            "crisp": "float"
        },
        "rules": {
            "standalone_impact": False,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_NUMBER,
            "section": SEC_DATA,
            "range_min": "poor",
            "range_max": "good",
            "help": "How well discretizable are the numerical Features of Interest? Discretizability is given if the data points of a feature distribution can be divided into intervals of equal size (equal-width binning) with a similar number of data points, or into bins with equal frequency (e.g. deciles/quartiles) with a similar width. This will not be taken into consideration if no Features of Interests are given!",
            "initialValue": 0,
            "min": 0,
            "max": 1,
            "rating": RATING_BAD,
            "conditionalRender": "foi"
        }
    },

    # preferences

    "perf_pref": {
        "label": "Performance Preference",
        "universe": u_10,
        "mem_funcs": m_tri_3_10,
        "rating": rating_3,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "str",
            "crisp": "str"
        },
        "rules": {
            "standalone_impact": False,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_RANGE,
            "section": SEC_PREFS,
            "range_min": "doesn't matter",
            "range_max": "high",
            "help": "How complex may the calculation of the XAI method be (regarding resource consumption)?",
            "initialValue": 0,
            "min": 0,
            "max": 10,
            "rating": RATING_AMOUNT
        }
    },
    "prep_time": {
        "label": "Preparation Time Preference",
        "universe": u_10,
        "mem_funcs": m_tri_3_10,
        "rating": rating_3,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "str",
            "crisp": "str"
        },
        "rules": {
            "standalone_impact": True,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_RANGE,
            "section": SEC_PREFS,
            "range_min": "fast",
            "range_max": "doesn't matter",
            "help": "How much time is available for method preparation and familiarization? If 'high' is inserted, effortful methods are not preferred, but are more likely to be considered good.",
            "initialValue": 0,
            "min": 0,
            "max": 10,
            "rating": RATING_DURATION
        }
    },

    # boolean
    "labels": {
        "label": "Labels available",
        "type": EXCLUSION_CRIT,
        "dtypes": {
            "fuzzy": "bool",
            "crisp": "bool"
        },
        "frontend": {
            "type": INPUT_CHECKBOX,
            "section": SEC_DATA,
            "help": "Are the training labels available?",
            "initialValue": True,
            "rating": RATING_BOOL
        }
    },
    "ordinal_feat": {
        "label": "Ordinal Features",
        "universe": u_bool, "mem_funcs": m_bool,
        "rating": rating_bool,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "bool",
            "crisp": "bool"
        },
        "rules": {
            "standalone_impact": False,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_CHECKBOX,
            "section": SEC_DATA,
            "help": "Does the dataset contain ordinal features?",
            "initialValue": False,
            "rating": RATING_BOOL
        }
    },
    "scope_local": {
        "label": "Local Scope",
        "universe": u_bool,
        "mem_funcs": m_bool,
        "rating": rating_bool,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "bool",
            "crisp": "bool"
        },
        "rules": {
            "standalone_impact": True,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_CHECKBOX,
            "section": SEC_PREFS,
            "help": "Are XAI methods preferred that provide local explanations, i.e. that explain the prediction of a specific data instance? (Global methods won't get rated worse)",
            "initialValue": True,
            "rating": RATING_BOOL
        }
    },
    "scope_global": {
        "label": "Global Scope",
        "universe": u_bool,
        "mem_funcs": m_bool,
        "rating": rating_bool,
        "type": RATING_CRIT,
        "dtypes": {
            "fuzzy": "bool",
            "crisp": "bool"
        },
        "rules": {
            "standalone_impact": True,
            "disable_processing": False
        },
        "frontend": {
            "type": INPUT_CHECKBOX,
            "section": SEC_PREFS,
            "help": "Are XAI methods preferred that provide global explanations of the entire system, independent of any specific input?",
            "initialValue": True,
            "rating": RATING_BOOL
        }
    },
    "foi_available": {
        "label": "FOI available",
        "type": RATING_CRIT,
        "rules": {
            "standalone_impact": False,
            "disable_processing": True
        },
        "universe": u_bool,
        "mem_funcs": m_bool,
        "rating": rating_bool,
    },
    # init rule
    "init": {
        "label": "Init Rule",
        "type": RATING_CRIT,
        "rules": {
            "standalone_impact": False,
            "disable_processing": True
        },
        "universe": u_bool,
        "mem_funcs": m_bool,
        "rating": rating_bool
    },

}
