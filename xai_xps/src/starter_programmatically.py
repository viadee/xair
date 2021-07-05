from XAIRecommender import XAIRecommender

example_inputs = {
        "model": True,
        "classif": True,
        "labels": False,
        "prep_ops": True,
        "predict_proba": True,
        "ordinal_feat": True,
        "scope_global": False,
        "scope_local": True,
        "foi": ["sex"],
        "corr": 0.7,
        "corr_foi": 0.68,
        "discr": 0.12,
        "discr_foi": 0.2,
        "perf_pref": 9,         # note: either insert fuzzy-values for criteria which is not data-related crisp ....
        "num_feat": 1,
        "dur_call": "M",        # ... ore use fuzzy term ("L", "M", "H")
        "prep_time": "M",

    }

if __name__ == '__main__':

    recommender = XAIRecommender(verbose=True, reload=True)
    #recommender.print_rules()

    output, processed_inputs = recommender.make_recommendation(example_inputs, return_inputs=True)
    print("-- Processed inputs:")
    print(processed_inputs)
    print("-- Output:")
    print(output)

    # plot output membership
    #recommender.plot_output_membership([o["label"] for o in output],save=True)

    print("-- Active rules for ALE:")
    _, rules = recommender.get_active_rules("ALE")
    [print("  ",r) for r in rules]
