import os
import sys
import pickle
import json

from flask import request, Flask

app = Flask(__name__)

current_dir = os.path.dirname(__file__)
pipe = pickle.load(open(os.path.join(current_dir, 'atm_pipe.pkl'), 'rb'))
model = pickle.load(open(os.path.join(current_dir, 'atm_model.pkl'), 'rb'))


@app.route('/atml/api/v1/predict', methods=['POST'])
def predict():

    X_test = pickle.loads(request.get_data())

    model_input = pipe.transform(X_test)
    prediction = model.predict(model_input)

    print (prediction)
    return  json.dumps(prediction.tolist())

@app.route('/atml/api/v1/score', methods=['POST'])
def score():

    score_input = pickle.loads(request.get_data())

    X = pickle.loads(score_input['X'])
    y = pickle.loads(score_input['y'])

    model_input = pipe.transform(X)
    score = model.score(model_input, y)

    return {'score': score}

if __name__ == '__main__':
    port = sys.argv[1]
    app.run(port=port)