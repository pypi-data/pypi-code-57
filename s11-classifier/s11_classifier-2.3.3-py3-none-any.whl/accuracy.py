"Accuracy assessment and plotting for classifier"
import itertools
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, cohen_kappa_score

def write_confusion_matrix(model_dict, test_set, cm_fn, plot=True):
    """ Uses a sklearn confusion matrix (np 2d array) to write to a csv file
    that also contains overall metrics. Also plots the confusion matrix for
    easier viewing.

        Args:
            cm The sklearn confusion matrix
            cm_labels  The labels in the confusion matrix
            cm_fn The filename of the output csv
            plot Whether or not to plot the figure

        returns:
            nothing
            """
    # Write and plot confusion Matrix
    x_test = test_set[[x for x in test_set.columns if 'class' not in x]].values
    y_test = np.ravel(
        test_set[[x for x in test_set.columns if 'class' in x]].values)
    all_classes = model_dict['labels']
    preds = model_dict['model'].predict(x_test)
    cm_labels = sorted(list(set(np.unique(y_test)) | set(np.unique(
        all_classes))))
    kappa = cohen_kappa_score(y_test, preds, labels=cm_labels)
    conf_matrix = confusion_matrix(y_test, preds, labels=cm_labels)
    df_cm = pd.DataFrame(data=conf_matrix, index=cm_labels, columns=cm_labels)
    metrics_list = []
    # Overall mean accuracy
    metrics_list.append('Overall Accuracy {:.4f}'.format(
        np.trace(conf_matrix)/np.nansum(conf_matrix)))
    metrics_list.append('Kappa {:.4f}'.format(kappa))

    # Total of the rows
    df_cm['Total'] = df_cm.sum(axis=1)
    # Accuracy
    df_cm['Accuracy'] = np.diag(df_cm[cm_labels]) / df_cm['Total']
    # Appending the numbers to the df
    df_cm = df_cm.append(df_cm.sum(axis=0).rename('Total')).append(
        (pd.Series(np.diag(conf_matrix) / np.sum(conf_matrix, axis=0),
                   index=cm_labels).rename('Reliability')))
    accuracy_logger = logging.getLogger(__name__)
    accuracy_logger.info("\n####-----Accuracy Assessment-----#####\n")
    df_cm.to_csv(cm_fn+'.csv', sep=';', float_format='%.4f')
    # Plotting if necessary
    if plot:
        try:
            # Plot normalized confusion matrix
            plt.figure()
            plot_confusion_matrix(conf_matrix,
                                  classes=cm_labels,
                                  normalize=True
                                 )
            plt.savefig(cm_fn + '_plot.png', dpi=150)
        except AttributeError:  # Not all models have FIs, so skip
            pass


def plot_confusion_matrix(conf_matrix, classes,
                          normalize=False,
                          cmap=plt.cm.Blues,
                          labeldict=None):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        conf_matrix = conf_matrix.astype('float') /\
                      conf_matrix.sum(axis=1)[:, np.newaxis]
    if labeldict is not None:
        classes = map(labeldict.get, classes)
    plt.imshow(conf_matrix, interpolation='nearest', cmap=cmap)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90, fontsize=6)
    plt.yticks(tick_marks, classes, fontsize=8)

    fmt = '.2f' if normalize else 'd'
    thresh = conf_matrix.max() / 2.
    for i, j in itertools.product(range(conf_matrix.shape[0]),
                                  range(conf_matrix.shape[1])):
        plt.text(j, i, format(conf_matrix[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if conf_matrix[i, j] > thresh else "black",
                 fontsize=4)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def plot_feature_importances(model_dict, outfile):
    """ Plot the feature importances of the forest"""
    importances = model_dict['model'].feature_importances_
    indices = np.argsort(importances)[::-1]
    labels = [model_dict['names'][x] for x in indices]
    nr_features = len(model_dict['names'])
    fig, axis = plt.subplots()
    axis.set_title("Feature importances (band numbers)")
    # Get STD whenever possible
    if model_dict['app_algorithm'] == 'randomforest':
        std = np.std([tree.feature_importances_ for tree in model_dict[
            'model'].estimators_], axis=0)
        axis.bar(range(nr_features), importances[indices],
                 color="r", yerr=std[indices], align="center")
    else:
        axis.bar(range(nr_features), importances[indices],
                 color="r", align="center")
    axis.set_xticks(range(nr_features))
    axis.set_xticklabels(labels, rotation=45, ha="right")
    axis.set_xlim([-1, nr_features])
    fig.tight_layout()
    plt.savefig(outfile, dpi=300)
