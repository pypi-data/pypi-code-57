import pickle
import pandas as pd
from models import QSAR_Autoencoder, QSAR_Classifier
import QSAR_Loss
import preprocessing
import outputs
import helper

import matplotlib.pyplot as plt

import numpy as np
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf

tf.random.set_seed(0)


pd.options.mode.chained_assignment = None


class ProteinClassifier():
    def __init__(self, features, ae_weight_path, cl_weight_folder_path):
        """[summary] This is the main class used to train and predict

        :param features: [description], defaults to 'clean'. It sets which version of data preprocessing to use
        :type features: str, optional
        :param weight_path: [description], Path where weights are stored
        :type weight_path: str, optional
        :raises Exception: [description] If files are not valid
        """
        self.features = features
        if self.features == 'clean':
            self.conv_dim = [20480, 300, 150, 100, 100, 80, 60, 15]
        elif self.features == 'raw':
            self.conv_dim = [22720, 300, 150, 100, 100, 80, 60, 15]
        else:
            raise Exception('Please enter a valid argument for features')
        self.ae_weight_path = ae_weight_path
        self.cl_weight_path = cl_weight_path

        ae_model_obj = autoencoder(self.conv_dim)
        self.conv_ae_model = ae_model_obj.conv_ae_model
        self.conv_ae_encoder = ae_model_obj.conv_ae_encoder
        self.conv_ae_model.load_weights(self.ae_weight_path)
        self.classifiers_list = self.create_classifiers(self.cl_weight_path)

        # optimizer = tf.keras.losses.BinaryCrossentropy(label_smoothing=0.1)
        # self.optimizer_nn = SGD(lr=0.001, momentum=0.7)

    def create_classifiers(self, cl_weight_folder_path):
        classifiers_list = []
        for i in range(9):
            clf = classifier.neuralNetworkClassifier()
            clf.compile(optimizer=self.optimizer_nn,
                        loss='binary_crossentropy')
            clf.load_weights(cl_weight_folder_path)
            classifiers_list.append(clf)
        return classifiers_list

    # def get_stats_file(self, file_path: str) -> object:
    #     """[summary] This function reads statistics file
    #
    #     :param file_path: [description]
    #     :type file_path: str
    #     :return: [description]
    #     :rtype: object
    #     """
    #     stats = pd.read_csv(file_path)
    #     stats.index = stats[stats.columns[0]]
    #     stats.drop(stats.columns[0], axis=1)
    #     return stats

    def preprocess(self, path=None, uniprot=None, train=False):
        """[summary] This function reads all the csv files from a path and preprocesses it

        :param path: [description], defaults to None. Describes path to csv files containing data
        :type path: [type], optional str
        :param uniprot: [description], defaults to None. Used if we want to make predictions on only a few uniprots.
        :type uniprot: [type], optional. List
        :param train: [description], defaults to False. Flag that is set for training
        :type train: bool, optional
        :raises Exception: [description] If the uniprot mentioned is not found in csv
        :raises Exception: [description] If folder path is invalid
        :return: [description]
        :rtype: [type]
        """

        if path is None and uniprot is None:
            raise Exception(
                'Please enter a folder path. Example "data/"\n or enter a list of Uniprots')

        subsample = False  # uses the whole csv in the path if set to false

        # check if we need to search by uniprot
        if type(uniprot) == list:
            subsample = True

            # load only required rows
            data_ed = helper.find_rows_with_uniprots(
                path + 'evolutionary_distance.csv', uniprot)
            data_phy = helper.find_rows_with_uniprots(
                path + 'bio_chemical.csv', uniprot)
            data_exp = helper.find_rows_with_uniprots(
                path + 'expression.csv', uniprot)
            data_bio = helper.find_rows_with_uniprots(
                path + 'cell_biology.csv', uniprot)

            if data_ed.shape[0] == 0:
                # Empty dataframe
                raise Exception(
                    'No Uniprot found in evolutionary_distance.csv')

        elif uniprot is None:
            # Read the whole file
            data_ed = pd.read_csv(path + 'evolutionary_distance.csv')
            data_phy = pd.read_csv(path + 'bio_chemical.csv')
            data_exp = pd.read_csv(path + 'expression.csv')
            data_bio = pd.read_csv(path + 'cell_biology.csv')

        # Extract and process files
        # Seperated into integer and float to avoid memory crash

        data_ed_flt, data_ed_int, uniprot_ed = helper.process_ed_csv(data_ed)
        data_ed = pd.concat([data_ed_flt, data_ed_int, uniprot_ed], axis=1)

        data_phy_flt, data_phy_int, uniprot_phy = helper.process_phy_csv(
            data_phy)
        data_phy = pd.concat([data_phy_flt, data_phy_int, uniprot_phy], axis=1)

        data_num, data_cat, uniprot_exp = helper.process_exp_csv(data_exp)
        data_exp = pd.concat([data_num, data_cat, uniprot_exp], axis=1)

        data_bio, uniprot_bio = helper.process_bio_csv(data_bio)
        data_bio = pd.concat([data_bio, uniprot_bio], axis=1)

        # merging all files
        data = pd.merge(data_exp, data_bio, on='Uniprot', sort=False)
        data = pd.merge(data, data_phy, on='Uniprot', sort=False)
        data = pd.merge(data, data_ed, on='Uniprot', sort=False)

        print(data.shape)
        print(data.select_dtypes('float32').shape)
        print(data.select_dtypes('int32').shape)

        # removing uniprot from columns
        final_uniprot = data['Uniprot']
        data.drop('Uniprot', axis=1, inplace=True)

        scaler_flt = helper.get_scaler('data/stats/scaler_flt.pkl')
        scaler_int = helper.get_scaler('data/stats/scaler_int.pkl')

        columns_flt = pd.read_csv('data/stats/data_flt.csv')
        columns_int = pd.read_csv('data/stats/data_int.csv')

        data_flt = data[columns_flt.Columns]
        data_int = data[columns_int.Columns]

        data_flt = preprocessing.minmax(
            data_flt, scaler=scaler_flt, dtype='float32')
        data_int = preprocessing.minmax(
            data_int, scaler=scaler_int, dtype='int32')

        data = pd.concat([data_flt, data_int], axis=1)

        final_columns = pd.read_csv('data/stats/final_columns.csv')
        data = data[final_columns['Columns']]

        data['Uniprot'] = final_uniprot
        return data

    def predict(self, data, weight_path='weights'):
        """[summary] This function makes predictions on preprocessed data

        :param data: [description] dataframe of pre-processed data
        :type data: [type] dataframe
        :param weight_path: [description], defaults to 'weights' Path where weights are stored
        :type weight_path: str, optional
        :return: [description] Dataframe containing predictions for uniprots
        :rtype: [type] dataframe
        """
        if weight_path != 'weights':
            print('Initializing model')
            self.optimizer = SGD(lr=0.001, momentum=0.7)

            self.model, self.encoder = autoencoder.model(self.conv_dim)

            self.model.compile(optimizer=self.optimizer,
                               loss={
                                   'decoded': 'binary_crossentropy',
                                   'enc_out': loss.triplet_semihard_loss
                               },
                               loss_weights={
                                   'decoded': 1.0,
                                   'enc_out': 1.0
                               }

                               )

            self.model.load_weights(
                weight_path + '/CAE clean/conv_ae weights bce.hdf5')

            # optimizer = tf.keras.losses.BinaryCrossentropy(label_smoothing=0.1)
            self.optimizer_nn = SGD(lr=0.001, momentum=0.7)

            self.classifiers = []
            for i in range(9):
                clf = classifier.neuralNetworkClassifier()
                clf.compile(optimizer=self.optimizer_nn,
                            loss='binary_crossentropy')
                clf.load_weights(
                    weight_path + f"/Neural network/classifier {i} weights.hdf5")
                self.classifiers.append(clf)

        self.encoder.trainable = False
        latent = self.encoder.predict(data)
        latent = latent.reshape((latent.shape[0], -1))
        predictions = []
        for i, clf in enumerate(self.classifiers):
            # making prediction
            predictions += [clf.predict(latent).reshape(1, -1)[0]]
        return predictions

    def fit_autoencoder(self, data, label, output_path='outputs', epochs=100):
        """[summary] This function trains the autoencoder on preprocessed data

        :param data: [description] Dataframe of preprocessed data
        :type data: [type] dataframe
        :param label: [description] Labels used for data
        :type label: [type] Series
        :param output_path: [description], defaults to 'outputs' Path where we want to store outputs
        :type output_path: str, optional
        :param epochs: [description], defaults to 100 Number of epochs to train model
        :type epochs: int, optional
        :return: [description] History object from the model
        :rtype: [type] object
        """
        self.model.trainable = True
        self.encoder.trainable = True

        checkpoint = ModelCheckpoint(output_path + 'ae_checkpont.hd5', 
                                     monitor='loss', verbose=False,
                                     save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        data = preprocessing.reshape(data)

        ae_history = self.model.fit(data,
                                    {'decoded': data,
                                     'enc_out': label
                                     },
                                    epochs=epochs, shuffle=True, 
                                    callbacks=callbacks_list, 
                                    use_multiprocessing=True, )

        fig = plt.figure(figsize=(16, 10))

        plt.plot(ae_history.history['loss'])

        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Loss', 'val_loss'], loc='upper left')
        plt.show()
        plt.savefig(output_path + 'Autoencoder_loss.png')

        self.model.save_weights(output_path + 'ae weights.hd5')

        return ae_history

    def fit_classifier(self, positive_uniprot_path, negative_uniprot_path, 
                       secreted_uniprot_path, data, save_path):
        """[summary] This function fit's the classifier on data

        :param positive_uniprot_path: [description] Path to positive labels
        :type positive_uniprot_path: [type] string
        :param negative_uniprot_path: [description]  Path to negative labels
        :type negative_uniprot_path: [type] string
        :param secreted_uniprot_path: [description] Path to secreted labels
        :type secreted_uniprot_path: [type] string
        :param data: [description] Preprocessed data
        :type data: [type] dataframe
        :param save_path: [description] Where to save the weights
        :type save_path: [type] str
        :return [description] History objects from the classifiers
        :type list
        """
        pos_uniprot_m = pd.read_csv(positive_uniprot_path)
        neg_uniprot = pd.read_csv(negative_uniprot_path)

        batch_feat = []
        batch_label = []
        for i in range(0, 9):
            if i < 8:
                positives = pos_uniprot_m[i * 10:(i + 1) * 10]
            else:  # if = 8
                positives = pos_uniprot_m[80:]
            pos_feat = data[data['Uniprot'].isin(positives)].drop(
                labels=['Uniprot'], axis=1)
            batch_feat += [
                pos_feat.append(data[data['Uniprot'].isin(neg_uniprot)].drop(
                    labels=['Uniprot'], axis=1))]
            label = pd.Series(data=np.ones(len(pos_feat))).append(
                pd.Series(data=np.zeros(10)))
            batch_label += [label.to_numpy()]

        self.encoder.trainable = False

        classifiers = []
        loss = []
        for i, (batch_data, label) in enumerate(zip(batch_feat, batch_label)):
            print("="*20)
            print("training", str(i), "th", "model")
            # Reinitializing weights
            clf = classifier()
            clf.compile(optimizer=self.optimizer_nn,
                        loss='binary_crossentropy')

            # Reshaping array for convolutional autoencoder
            batch_data = preprocessing.reshape(batch_data)

            # Find embeddings of training set from encoder
            latent = self.encoder.predict(batch_data)
            latent = latent.reshape((latent.shape[0], -1))

            shuffle_idx = np.random.permutation(latent.shape[0])

            class_weight = [1, 1]

            history = clf.fit(latent[shuffle_idx], label[shuffle_idx],
                              epochs=50, class_weight=class_weight)

            loss += [history.history['loss']]

            classifiers.append(clf)

            for i, c in enumerate(classifiers):
                c.save_weights(save_path + f"/classifier {i} weights.hdf5")

            return loss


pc = ProteinClassifier()
data = pc.preprocess('data/', uniprot=['Q9UHF1', 'O95967', 'Q2TAL6', 'Q6UXX9'])

uniprot = data['Uniprot']
data = data.drop('Uniprot', axis=1)

data = preprocessing.reshape(data)
preds = pc.predict(data)
output = outputs.prediction_df(preds, uniprot)
print(output)
