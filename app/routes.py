from flask import jsonify, request
from app import app
from .helpers import create_index, retrieve_pipeline

@app.route('/', methods=['POST'])
def index():
    if request.method != 'POST':
        # Method not allowed
        return jsonify(error="Method not allowed"), 405

    # Get the text data from the request
    data = request.data.decode('utf-8')

    query = f"""
        Assume you're a patient with limited medical knowledge.
        You've received an MRI scan report, but it's filled with complex medical jargon.
        You want the report explained to you in plain English so you can understand it better.
        Break down the MRI findings and explain any abnormalities or conditions detected.
        Include details on what each part of the MRI image represents and how it relates to your health.
        Provide insights into potential treatment options or further diagnostic tests based on the MRI findings.
        Provide clarification on any terms or concepts you're unfamiliar with.
        
        Medical report: {data} 
        """

    answer = retrieve_pipeline(query=query)

    # Prepare the response data
    response_data = {
        "message": answer,
    }

    # Return the response
    return jsonify(status=200, response=response_data), 200

@app.route('/build-index', methods=['GET'])
def build_index():
    if request.method != 'GET':
        # Method not allowed
        return jsonify(error="Method not allowed"), 405

    create_index()

    # Prepare the response data
    response_data = {
        "message": "Vector DB set up successfully!",
    }

    # Return the response
    return jsonify(status=200, response=response_data), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=404, text=str(e)), 404