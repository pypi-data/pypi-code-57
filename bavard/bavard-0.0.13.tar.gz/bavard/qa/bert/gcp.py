from official.nlp.bert.tokenization import FullTokenizer

from bavard.gcp.online_prediction import predict_json
from bavard.qa.bert.input_preprocessing import raw_input_to_features
from bavard.qa.bert.predict import QAPredictor
from bavard.qa.bert.raw_input import RawInput


def bert_qa_online_prediction(context: str, question: str, tokenizer: FullTokenizer):

    raw_input = RawInput(question=question, context=context, is_training=False)

    input_features = raw_input_to_features(tokenizer=tokenizer,
                                           raw_input=raw_input,
                                           max_seq_len=384,
                                           max_question_len=64,
                                           stride=128,
                                           is_training=False)

    instances = []

    for features in input_features:
        x = {}
        for (k, v) in features.to_prediction_input().items():
            values = v.numpy()[0].tolist()
            x[k] = values
        instances.append(x)

    preds = predict_json(project='bavard-dev', model='bert_qa', instances=instances, version='bert_qa_v1')

    context_words = context.split()
    best_score = float('-inf')
    best_ans = ''

    for (i, p) in enumerate(preds):
        ans_start = p['ans_start']
        ans_end = p['ans_end']
        ans, score = QAPredictor.decode_prediction(context_words, input_features[i], ans_start, ans_end)
        if score > best_score:
            best_score = score
            best_ans = ans

    return best_ans
