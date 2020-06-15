from bavard.gcp.online_prediction import predict_json
from bavard.text_summarization.extractive.bert.model import ExtractiveSummarizer
from bavard.text_summarization.extractive.bert.input_preprocessing import raw_input_to_features
from official.nlp.bert.tokenization import FullTokenizer


def bert_extractive_summary_online_prediction(
        project: str,
        model: str,
        model_version: str,
        article: str,
        max_words: int,
        tokenizer: FullTokenizer):
    input_features = raw_input_to_features(tokenizer=tokenizer,
                                           article=article,
                                           max_seq_len=512,
                                           max_sentences=20,
                                           is_training=False)

    predictions = []
    for feature in input_features:
        instances = []

        instance = {}
        x, _ = feature.to_prediction_input()
        for (k, v) in x.items():
            values = v.numpy()[0].tolist()
            instance[k] = values
        instances.append(instance)

        pred = predict_json(project=project, model=model, instances=instances, version=model_version)

        predictions.append(pred)

    return ExtractiveSummarizer.decode_predictions(inputs=input_features,
                                                   predictions=predictions,
                                                   max_words=max_words)
