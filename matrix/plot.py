# ### Confusion Matrix Grafiği
import numpy as np
import itertools
import matplotlib.pyplot as plt

np.set_printoptions(precision=2)


def plot_confusion_matrix(cm, classes=None,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues,
                          x_label=None,
                          y_label=None):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if classes is None:
        classes = ['up', 'const', 'down']
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=0)
    #    print("Normalized confusion matrix")
    else:
        pass
    #    print('Confusion matrix, without normalization')

    # print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    x_class = np.array(classes)[[0, 2]]
    y_class = np.array(classes)

    x_tick_marks = np.arange(len(x_class))
    y_tick_marks = np.arange(len(y_class))

    plt.xticks(x_tick_marks, x_class, rotation=45)
    plt.yticks(y_tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.tight_layout()

    return plt
