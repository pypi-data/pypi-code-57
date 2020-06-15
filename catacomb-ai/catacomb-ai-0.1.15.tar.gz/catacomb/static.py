DOCKERFILE = """
FROM python:3.7-slim

RUN apt-get update && apt-get install --no-install-recommends -y gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install 'pipenv==2018.11.26'

WORKDIR /app

# Copy project dependencies
COPY Pipfile* /app/

# Install project dependencies
RUN pipenv install --deploy

# Copy project files
COPY . /app/

RUN test -e catacomb.sh && bash catacomb.sh || true

ENTRYPOINT ["sh", "-c"]

CMD ["pipenv run python /app/server.py"]
"""

SERVER = """
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from system import *

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

system = System()

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
  return response

@app.route("/predict", methods=['POST', 'OPTIONS', 'GET'])
def predict():
    input_object = request.get_json()['input']
    return jsonify(output=system.output(input_object))

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)), debug=True)
"""