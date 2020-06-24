DOCKERFILE = """
# syntax = docker/dockerfile:1.1.7-experimental
FROM python:3.7-slim

RUN apt-get update && apt-get install --no-install-recommends -y gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install 'pipenv==2018.11.26'

WORKDIR /app

# Copy project dependencies
COPY Pipfile* /app/

# Install project dependencies
RUN --mount=type=cache,target=/root/.cache pipenv install --deploy

# Copy project files
COPY . /app/

COPY catacomb-out/server.py /app/

RUN test -e catacomb.sh && bash catacomb.sh || true

ENTRYPOINT ["sh", "-c"]

CMD ["pipenv run python /app/server.py"]
""".strip()

SERVER = """
import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from system import *

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

system = System()

@app.route("/predict", methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def predict():
    input_object = request.get_json()['input']
    return jsonify(output=system.output(input_object))

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)), debug=True)
""".strip()