import os

import click
from official.nlp.bert import tokenization
import tensorflow_hub as hub
from bavard.qa.bert.input_preprocessing import raw_input_to_features

from bavard.qa.bert.raw_input import RawInput
from bavard.qa.bert.gcp import bert_qa_online_prediction as get_bert_qa_online_prediction
from bavard.qa.bert.predict import QAPredictor
from bavard.qa.bert.squad2.train import BertSquadTrainer
from bavard.gcp.online_prediction import predict_json
from bavard.text_summarization.extractive.bert.cnndm.data_loader import ExtractiveDataLoader
from bavard.text_summarization.extractive.bert.model import ExtractiveSummarizer

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
tf.get_logger().setLevel('ERROR')


from . import bert_squad2_features as bert_squad2


@click.group()
def qa():
    pass


@qa.command()
@click.option('--vocab-path', type=click.Path(exists=True))
@click.option('--squad-path', type=click.Path(exists=True))
@click.option('--is-training', is_flag=True, default=False)
@click.argument('output-path', type=click.Path())
def squad2_tf_features_for_bert(vocab_path: str, squad_path: str, is_training: bool, output_path: str):
    bert_squad2.squad2_tf_features_for_bert(vocab_path, squad_path, is_training, output_path)


@qa.command()
@click.option('--squad-train', type=click.Path(exists=True), help="Path to the squad train tf-record file")
@click.option('--bert-dir', type=click.Path(exists=True), help="Directory that contains the BERT model and config")
@click.option('--checkpoint-dir', type=click.Path(exists=False), help="Directory in which to save model checkpoints")
@click.option('--batch-size', type=int, default=2)
@click.option('--steps-per-epoch', type=int, default=300)
@click.option('--epochs', type=int, default=500)
def train_bert_squad(squad_train: str,
                     bert_dir: str,
                     checkpoint_dir: str,
                     batch_size: int,
                     steps_per_epoch: int,
                     epochs: int):
    bert_squad_trainer = BertSquadTrainer(squad_train=squad_train, bert_dir=bert_dir, saved_model_dir=checkpoint_dir)
    bert_squad_trainer.train(batch_size=batch_size, steps_per_epoch=steps_per_epoch, epochs=epochs)


@qa.command()
@click.option('--bert-dir', type=click.Path(exists=True))
@click.option('--checkpoint-dir', type=click.Path(exists=True))
@click.option('--context-file', type=click.Path(exists=True))
def bert_qa_repl(bert_dir: str, checkpoint_dir: str, context_file: str):
    predictor = QAPredictor(bert_dir=bert_dir, checkpoint_dir=checkpoint_dir)

    context = open(context_file, 'r').read().strip()
    print("context: ", context)
    while True:
        question = str(input(">"))
        question = question.lower()

        if question == "exit":
            click.echo("Bye!")
            break

        ans = predictor.get_answer(context, question)

        if ans:
            click.echo(ans)
        else:
            click.echo("Sorry, unable to answer that.")


@qa.command()
@click.option('--context', type=str, required=True)
@click.option('--question', type=str, required=True)
def bert_qa_online_prediction(context: str, question: str):
    bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=True)
    vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
    tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

    answer = get_bert_qa_online_prediction(context=context, question=question, tokenizer=tokenizer)
    click.echo(answer)
