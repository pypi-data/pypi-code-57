"""This model designed to preprocess data and
it has many features to help users to minimize their codes for
preprocessing purposes!
"""
import os
import json
import logging
import codecs


class PreProcess:
    """ for testing
    """
    def __init__(self, config):
        self.sentences = []
        self.words = []
        self.result = []
        self.stem_words = []
        self.lemmatized_words = []
        self.non_stopwords = []
        self.data = config['text']
        self.language = config['Language']
        self.dataset_type = config['DatasetType']
        self.input_path = config['InputFilePath']
        self.output_path = config['OutputFilePath']

    def sent_tokenize(self):
        """
        :return:
        """
        self.sentences = self.model.sent_tokenize(self.data)
        print('the result of sent tokenize is = {}'.format(self.sentences))

    def word_tokenize(self):
        """
        :return:
        """
        self.words = [self.model.word_tokenize(sent) for sent in self.sentences]
        print('the result of word tokenize is = {}'.format(self.words))

    def lemmatize(self):
        pass

    def stem(self):
        pass

    def write_to_file(self):
        """
        :param path:
        :return:
        """
        path = os.getcwd() + '/output.json'
        with open(path, 'w') as outfile:
            json.dump(self.data, outfile)
        logging.getLogger().setLevel(logging.INFO)
        logging.info(f'the result has been saved in {path}')
        return self.data

    def read_from_file(self, path=''):
        """
        :param path:
        :return:
        """
        if path:
            with open(path) as json_file:
                self.data = json.load(json_file)

    # def __set_raw_text(self):
    #     with codecs.open(self.input_path, 'r', encoding='utf-8') as file:
    #         self.text = file.read()
    #
    # def write_preprocessed_text(self):
    #     text = []
    #     text = "<SENT>" + '\n<SENT>'.join([' '.join(sent + ["</SENT>"]) for sent in self.result])
    #     with codecs.open(self.output_path, 'w', encoding='utf-8') as file:
    #         file.write(text)
