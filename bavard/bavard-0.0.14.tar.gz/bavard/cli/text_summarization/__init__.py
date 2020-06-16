import click
import tensorflow as tf
import tensorflow_hub as hub
from official.nlp.bert import tokenization
from tqdm import tqdm
import os

from bavard.text_summarization.extractive.bert.model import ExtractiveSummarizer
from bavard.text_summarization.extractive.bert.cnndm.data_loader import ExtractiveDataLoader
from bavard.text_summarization.extractive.bert.gcp import bert_extractive_summary_online_prediction


@click.group()
def text_summarization():
    pass


@text_summarization.command()
@click.argument('output-path', type=click.Path())
def create_bert_cnndm_tf_record(output_path: str):
    bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=True)
    vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
    tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

    features = ExtractiveDataLoader.load_training_set(tokenizer)

    print(f'Loading CNN/DM examples. Writing TF records to {os.path.basename(output_path)}')
    writer = tf.io.TFRecordWriter(output_path)
    for i, input_feature in enumerate(tqdm(features)):
        writer.write(input_feature.serialize_to_string())
    writer.close()


@text_summarization.command()
@click.option('--saved-model-dir', type=click.Path(exists=False), help="Directory in which to save model checkpoints")
@click.option('--train-data-path', type=click.Path(exists=True), help="Path to the tf-record training set file")
@click.option('--input-len', type=int, default=512)
@click.option('--batch-size', type=int, default=1)
@click.option('--steps-per-epoch', type=int, default=500)
@click.option('--epochs', type=int, default=500)
def train_bert_extractive_summarizer(
        saved_model_dir: str,
        train_data_path: str,
        input_len: int,
        batch_size: int,
        steps_per_epoch: int,
        epochs: int):
    training_set = tf.data.TFRecordDataset([train_data_path])

    if os.path.exists(saved_model_dir):
        print('Loading saved model')
        model = tf.keras.models.load_model(saved_model_dir)
    else:
        model = ExtractiveSummarizer.build_model(input_len=input_len)

    ExtractiveSummarizer.compile_model(model)
    ExtractiveSummarizer.train(model=model,
                               ds=training_set,
                               batch_size=batch_size,
                               steps_per_epoch=steps_per_epoch,
                               epochs=epochs,
                               saved_model_path=saved_model_dir)


@text_summarization.command()
@click.option('--article-file', type=click.Path(exists=True))
@click.option('--saved-model-dir', type=click.Path(exists=True))
@click.option('--max-words', type=int, default=200)
def get_bert_summary(article_file: str, saved_model_dir: str, max_words: int):
    bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=True)
    vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
    tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)
    predictor = ExtractiveSummarizer(tokenizer=tokenizer, saved_model_dir=saved_model_dir)

    article = open(article_file, 'r').read().strip()
    summary = predictor.get_summary(text=article, max_words=max_words)
    click.echo(summary)


@text_summarization.command()
@click.option('--article-file', type=click.Path(exists=True))
@click.option('--max-words', type=int, default=200)
@click.option('--project', type=str, default='bavard-dev')
@click.option('--model', type=str, default='bert_ext_summarizer')
@click.option('--model-version', type=str, default='bert_ext_summ_v1')
def get_bert_summary_gcp(article_file: str, max_words: int, project: str, model: str, model_version: str):
    bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=True)
    vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
    tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

    article = open(article_file, 'r').read().strip()
    summary = bert_extractive_summary_online_prediction(project=project,
                                                        model=model, model_version=model_version, article=article,
                                                        max_words=max_words, tokenizer=tokenizer)
    click.echo(summary)
