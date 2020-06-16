import os

from official.nlp.bert.tokenization import FullTokenizer
from tqdm import tqdm

from bavard.qa.bert.feature_writer import FeatureWriter
from bavard.qa.bert.input_preprocessing import raw_input_to_features
from bavard.qa.bert.squad2.squad_data_loader import SquadDataLoader


def squad2_tf_features_for_bert(vocab_path: str, squad_path: str, is_training: bool, output_path: str):
    writer = FeatureWriter(output_path, is_training=is_training)

    raw_inputs = SquadDataLoader.read_examples(squad_path, is_training)

    print("Loading SQuAD2.0 examples.")
    raw_inputs = list(tqdm(raw_inputs))
    print(f'Writing TF records to {os.path.basename(output_path)}')

    tokenizer = FullTokenizer(vocab_file=vocab_path)

    for i, _input in enumerate(tqdm(raw_inputs)):
        inputs = raw_input_to_features(tokenizer=tokenizer,
                                       raw_input=_input,
                                       max_seq_len=384,
                                       max_question_len=64,
                                       stride=128,
                                       is_training=is_training)
        for x in inputs:
            writer.process_feature(x)

    writer.close()
