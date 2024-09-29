from flask import Flask, jsonify, request
from REFAIR import get_domain
from REFAIR import get_ml_task
from REFAIR import feature_extraction

app = Flask(__name__)

@app.route("/")
def homepage():
    return "Welcome to ReFair!"

@app.route('/refair', methods = ['POST','GET'])
def analysis():
    
    if request.method == 'POST':
        story = request.form['story']   
        domain = get_domain(story)
        ml_tasks = get_ml_task(story, domain)

        features = feature_extraction(domain, ml_tasks)

        return jsonify(
            domain=domain,
            tasks=ml_tasks,
            features=features
        )
    else: return "Not Allowed"
    