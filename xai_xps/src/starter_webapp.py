from Utils import get_config, CONFIG_FILE
from XAIRecommender import XAIRecommender
from XAIRInitializer import XAIRInitializer
from flask import Flask, request, send_from_directory
from flask_cors import CORS

# using flask instead of flask_restful, since there are only two routes
app = Flask(__name__)

# allowing all http requests and origins
cors = CORS(app)

recommender = XAIRecommender(verbose=False, reload=True)


@app.route('/xairecommender', methods=["POST"])
def post():
    """
        Receives POST request (e.g. from frontend application)
        @returns recommendation object for given request parameters
    """

    validator = recommender.rec_sim.input_validator

    inputs = request.get_json()


    if not validator.validate(inputs):
        return validator.errors, 400

    recommendation, inputs_processed = recommender.make_recommendation(inputs, return_inputs=True)

    excl = recommender.get_method_information()[1]
    html, _ = recommender.get_active_rules()

    return {
        "recommendation": recommendation,
        "active_rules": html,
        "excluded_methods": excl,
        "inputs_orig": inputs,
        "inputs_processed": inputs_processed
    }


@app.route("/config", methods=["GET"])
def get_configuration():
    """
        Get recommendation for given ID
    """
    dir, file_name = get_config().resource_files.frontend_input_config.rsplit("/", 1)
    print(f"dir: {dir}, file: {file_name}")
    return send_from_directory(dir, file_name)


if __name__ == '__main__':
    # run webapp
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
