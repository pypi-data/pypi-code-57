import json

import click
from official.nlp.bert import tokenization

from . import preprocessing
from ...chatbots.albert_intents_and_tags_model.model import AlbertIntentsAndTagsModel
import tensorflow_hub as hub

@click.group()
def chatbots():
    pass


@chatbots.command()
@click.option('--json-path', type=click.Path(exists=True), required=True)
@click.argument('output-path', type=click.Path())
def agent_data_to_tfrecord(json_path: str, output_path: str):
    preprocessing.agent_data_to_tfrecord(json_path=json_path, output_path=output_path)


@chatbots.command()
@click.option('--agent-data-file', type=click.Path(exists=True), required=True)
@click.option('--model-dir', type=click.Path(exists=True), required=True)
@click.option('--text', type=str, required=True)
def predict(agent_data_file: str, model_dir: str, text: str):
    with open(agent_data_file) as f:
        agent_data = json.load(f)

    intents = agent_data['intents']
    tag_types = agent_data['tagTypes']
    n_tags = len(tag_types) * 2 + 3  # B-Tag, I-Tag, O, CLS, SEP
    n_intents = len(intents)

    model = AlbertIntentsAndTagsModel(max_seq_len=200,
                                      n_tags=n_tags,
                                      n_intents=n_intents,
                                      saved_model_dir=model_dir,
                                      load_model=True)

    albert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/albert_en_base/1", trainable=False)
    sp_model_file = albert_layer.resolved_object.sp_model_file.asset_path.numpy()
    tokenizer = tokenization.FullSentencePieceTokenizer(sp_model_file)
    pred = model.predict(text=text, intents=intents, tag_types=tag_types, tokenizer=tokenizer)
    print(pred)


@chatbots.command()
@click.option('--train-file', type=click.Path(exists=True), help="Path to the tf-record file")
@click.option('--num-intents', type=int, help="Number of intent types", required=True)
@click.option('--num-tags', type=int, help="Number of tag types", required=True)
@click.option('--saved-model-dir', type=click.Path(exists=False), help="Directory in which to save model checkpoints")
@click.option('--batch-size', type=int, default=4)
@click.option('--steps-per-epoch', type=int, default=300)
@click.option('--epochs', type=int, default=5)
def train(train_file: str,
          num_intents,
          num_tags,
          saved_model_dir: str,
          batch_size: int,
          steps_per_epoch: int,
          epochs: int):
    model = AlbertIntentsAndTagsModel(max_seq_len=200,
                                      n_tags=num_tags,
                                      n_intents=num_intents,
                                      saved_model_dir=saved_model_dir)
    model.train(training_path=train_file, batch_size=batch_size, steps_per_epoch=steps_per_epoch, epochs=epochs)
