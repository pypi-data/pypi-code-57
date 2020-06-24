from akida.core import (Layer, InputDataParams, InputLayerParams, InputParams,
                        BackendType)


class InputData(Layer):
    """This is the general purpose input layer. It takes events in a simple
    address-event data format; that is, each event is characterized by a trio
    of values giving x, y and channel values.

    Regarding the input dimension values, note that AEE expects inputs with
    zero-based indexing, i.e., if input_width is defined as 12, then the model
    expects all input events to have x-values in the range 0–11.

    Where possible:

    - The x and y dimensions should be used for discretely-sampled continuous
      domains such as space (e.g., images) or time-series (e.g., an audio
      signal).

    - The c dimension should be used for ‘category indices’, where there is no
      particular relationship between neighboring values.

    The input dimension values are used for:

    - Error checking – input events are checked and if any fall outside the
      defined input range, then the whole set of events sent on that
      processing call is rejected. An error will also be generated if the
      defined values are larger than the true input dimensions.

    - Configuring the input and output dimensions of subsequent layers in the
      model.

    """

    def __init__(self, input_width, input_height, input_channels, name=""):
        """Create an ``InputData`` layer from a name and parameters.

        Args:
            input_width (int): input width.
            input_height (int): input height.
            input_channels (int): size of the third input dimension.
            name (str, optional): name of the layer.

        """
        try:
            params = InputDataParams(
                InputLayerParams(
                    InputParams(input_width, input_height, input_channels)))

            # Call parent constructor to initialize C++ bindings
            # Note that we invoke directly __init__ instead of using super, as
            # specified in pybind documentation
            Layer.__init__(self, params, name)
        except:
            self = None
            raise
