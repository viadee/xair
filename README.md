# eXplainable AI Recommender (XAIR)
... Should it be Anchors or SHAP? Or something else?

# Table of contents
1. [Why should I use this XAIR?](#why)
2. [Summary of benefits using the XAIR](#benefits)
3. [Installation guide](#installation)
4. [How can I participate in the development?](#participate)
5. [When is a XAI method "suitable"?](#method-suitability)
6. [How is the recommendation made?](#how-recommendation)
7. [TODOs](#todo)

<a name="why"></a>
## Why should I use this XAIR?

Recent XAI research has presented a variety of XAI methods and implementations in the form of stand-alone prototype solutions. However, these are hardly used in practice. This is partly because XAI is a new and rapidly developing field, and partly because the existing knowledge is scattered and needs to be organized.

Some scientific publications classify diverse methods hierarchically, but rarely provide concrete guidelines or advices for their application. Government agencies such as the German Federal Office for Information Security (BSI) point out the relevance of explainability of AI systems and that method-specific properties of inputs must be considered in the selection process, and plausible explanations must be enabled. However, it does not provide information to help users successfully select and apply an XAI method that is appropriate in this sense.

Not all XAI methods are ideally suited in all contexts of use. For example, results of perturbation-based methods can be falsely influenced by correlations in the input features.

The XAI Recommender (XAIR) considers all suitability-influencing parameters and suggests a suitable method for your data and model context. For the application, only vague knowledge about the training dataset and the context of use is assumed.

It simplifies the selection of an XAI method and its implementation by providing a well-founded recommendation. Moreover, you're also encouraged to actually apply the suggested XAI method by receiving detailed and targeted method information! 

Furthermore, it can be used as a standalone web application or automatically, e.g. within an ML pipeline. You can try the web application  <a href="http://xairecommender-frontend.germanywestcentral.azurecontainer.io/start/">here!</a>

<p align="center">
<img src="https://user-images.githubusercontent.com/55053898/122918931-f45cac00-d35f-11eb-9746-7ce29b356ac1.png" alt="screenshot" width="60%"/>
</p>

<a name="benefits"></a>
## TL;DR: Short summary of benefits using the XAIR

* Get a justified recommendation of an applicable XAI method
* Learn which XAI method should be used under which circumstances
* Get a suggested implementation with some hints for it’s application
* Inform yourself about all available XAI methods
* Learn German (sorry, information pages are currently not available in English)

<a name="installation"></a>
# Installation guide

Please clone repository first.

## Backend Project
Python and Pip are required for installation.

1. In the `xai_xps` directory install the `requirements.txt`: `pip install -r requirements.txt`
2. Now you can run it programmatically, e.g. by changing the example values in `src/starter_programmatically.py` or using the XAIR like that:

```python
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
        "foi": ["age"],
        "corr": 0.7,
        "corr_foi": 0.68,
        "discr": 0.12,
        "discr_foi": 0.2,
        "perf_pref": 9,         # note: either insert fuzzy-values for criteria which is not data-related crisp ....
        "num_feat": 1,
        "dur_call": "M",        # ... ore use fuzzy term ("L", "M", "H")
        "prep_time": "M",
    }

xair = XAIRecommender()
output, processed_inputs = xair.make_recommendation(example_inputs, return_inputs=True)
[print(f"Method '{o['name']}': rating: {o['rating']}") for o in output]

# print all rules
xair.print_rules()

# print all active rules for one output method
_, active_rules = xair.get_active_rules("ALE")

```

## Frontend Project
Node and NPM are required for installation.
1. In the `xai-recommender-frontend` directory install all npm requirements: `npm install`
2. In case you want to start a development server (enabling useful features like live reloading and Gatsby’s data explorer):
- Run `npm run develop`
- Open http://localhost:8000
3. In case of production-ready deployment: 
- Run `run npm build` to build the project
- To serve locally, run `npm run serve` (and open http://localhost:9000)
- ... Or move new `public` folder to deployment environment (e.g. nginx Server)

# Containerization with Docker

You can dockerize the front- and backend projects by using the Dockerfiles provided.
Please note, that the frontend Dockerfile has to be exectued one directory above (`xair/`, not in `xair/xai-recommender-frontend/`):
<br/>
`docker image build . -f ./xai-recommender-frontend/Dockerfile`


<a name="participate"></a>
# How can I participate in the development?

You are welcome to add new methods and/or newly identified criteria, or expand or edit existing knowledge (in the form of ratings regarding the criteria).
For adding something to the knowledge base, please take a look at `xai_xps/src/knowledge_acquisition.ipynb` (Jupyter Notebook installation required).

<a name="how"></a>
# How the system works

<a name="method-suitability"></a>
## When is a XAI method "suitable"?

The quality of an XAI method cannot be judged on the basis of the quality of the resulting explanation. This is highly contextual and subjective due to social beliefs and cognitive biases (Miller 2017).

Accordingly, it is defined by characteristics of the context of use that
* make the application of the XAI method difficult or impossible
* have a negative, distorting influence on a sound, coherent and reasonable explanation result due to the algorithmic nature of the XAI method
* reduce or complicate the interpretability of the explanation. 

A method rating can arise either because of (an aggregation of) positive and negative criteria evaluations, or by an absence of suitability-reducing criteria evaluations.

<b>
Results of the system must be seen in relative terms: Even the worst rated method can be suitable if all other methods were rated better due to the presence of suitability-increasing criteria.
  </b>
  
<a name="how-recommendation"></a>
## How is the recommendation made?

The XAI Recommender suggests you a XAI method that is the most appropriate for your specific context of use.

Unfortunately, no exact measurement of the strength/height of many input parameters is possible due to lack of thresholds (e.g. “correlation”: How can you measure the correlation of a complete data set?). Furthermore, the literature gives only vague estimates of method suitability with respect to these imprecise criteria, so only an approximate recommendation is possible.

Therefore, the recommendation system internally uses a fuzzy expert system.

Your crisp input, inserted via the range or the regular input field, will be transformed into a literary term. Depending on the truth of this term for the input value, fuzzy rules are activated to determine the suitability of all methods. The result of all fired rules is aggregated for each method and output as a crisp value reflecting the suitability of this method. So the fuzzy expert system’s result is a list of XAI methods and their suitabilities.

In a second step, methods that cannot be applied due to non-existing prerequisites, are removed from this list using boolean logic. All applicable methods, sorted by their suitability, will be issued!


<a name="todo"></a>
# TODO

* Receive feedback for method recommendations in order to improve the knowledge base and thus the recommendations 
