from . import core, optim, loss


def api(token):
    """Use this function to get access to the API, providing your token. All subsequents API calls will use this token.

        :param token: Token from dashboard
        :type token: str
    """
    core.api(token)


def compile(model, input_shape, library="", model_label="", asynchronous=False):
    """Use this to upload and compile your model. Compatible frameworks are:

        * Pytorch
        * Tensorflow 2
        * Mxnet

        :param model: Original model to compile.
        :type model: Object from framework or filename(str) to the model. `Tensorflow` + `mxnet` models must be tarred if using filenames.
        :param input_shape: Input shape of model
        :type input_shape: List
        :param library: Library used
        :type library: str (pytorch, tf, mxnet)
        :param model_label: Label for model
        :type model_label: str, optional
        :param asynchronous: If call should run async or not. Default=`False`
        :type asynchronous: bool, optional.

        :return: compiled model.
    """
    return core.compile(model, input_shape, library, model_label, asynchronous)


def predict(model, data, asynchronous=False, callback=None):
    """Perform a predict using a model. Default behaviour is synchronous.

        :param model: Model used to predict
        :type model: From :func:`npu.compile` or :func:`npu.train`. Id (str) or global :class:`npu.vision.models.Model` can be used.
        :param data: Data to be used for prediction
        :type data: numpy array
        :param asynchronous: If call should run async or not. Default=`False`. If you want to get the result back explicitly, call "get_result()" on returned value.
        :type asynchronous: bool, optional.
        :param callback: runs a callback function on results (asynchronous)
        :type callback: function
    """
    return core.predict(model, data, asynchronous, callback)


def train(model, train_data, val_data, batch_size=32, epochs=1, optim=optim.SGD(), loss=loss.SparseCrossEntropyLoss, asynchronous=False, callback=None):
    """Perform a train using a model. Default behaviour is synchronous.

        :param model: Model used to predict
        :type model: From :func:`npu.compile` or :func:`npu.train`. Id (str) or global :class:`npu.vision.models.Model` can be used.
        :param train_data: Training data in format of (x, y)
        :type train_data: numpy array
        :param val_data: Validation data in format of (x, y)
        :type val_data: numpy array
        :param batch_size: Batch size for training. Default=`32`
        :type batch_size: int, optional
        :param epochs: Epoch cycles for training. Default=`1`
        :type epochs: int, optional
        :param optim: Optimiser to use
        :type optim: :func:`npu.optim`
        :param loss: Loss function to use
        :type loss:
        :param asynchronous: If call should run async or not. Default=`False`. If you want to get the result back explicitly, call "get_result()" on returned value.
        :type asynchronous: bool, optional.
        :param callback: runs a callback function on results (asynchronous)
        :type callback: function
    """
    return core.train(model, train_data, val_data, batch_size, epochs, optim, loss, asynchronous, callback)


def export(model, path="."):
    """Export a model to file. This will export it in the original format it is in. Global models will be exported as
    pytorch models.

        :param model: Model to export
        :type model: From :func:`npu.compile` or :func:`npu.train`. Id (str) or global :class:`npu.vision.models.Model` can be used.
        :param path: Path to where the model is saved to. Default is ".".
        :type path: str, optional
    """
    return core.export(model, path)




