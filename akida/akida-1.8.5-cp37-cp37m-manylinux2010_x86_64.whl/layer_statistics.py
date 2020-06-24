import numpy as np
import weakref
from .core import Layer, LayerType


class LayerStatistics(object):
    """Container attached to an akida.Model and an akida.Layer that allows to
        retrieve layer statistics:
        (average input and output sparsity, number of operations, number of
        possible spikes, row_sparsity).

    """

    def __init__(self, model, layer, prev_layer=None):
        self._layer = layer
        self._prev_layer = prev_layer
        # a weakref to model to avoid circular reference
        self._model = weakref.ref(model)
        self._input_sparsity = 0
        self._output_sparsity = 0
        self._spiking_loop = 0

        def compute_stats(layer, source_id, spikes, potentials):
            try:
                if spikes is not None:
                    self._output_sparsity += spikes.sparsity
                self._spiking_loop += 1
            except Exception as e:
                # We swallow any python exception because otherwise it would
                # crash the calling library
                print("Exception in observer callback: " + str(e))

        self._id = model.register_observer(layer, compute_stats)

        if prev_layer is not None:

            def compute_stats_prev(layer, source_id, spikes, potentials):
                try:
                    if spikes is not None:
                        self._input_sparsity += spikes.sparsity
                except Exception as e:
                    # We swallow any python exception because otherwise it would
                    # crash the calling library
                    print("Exception in observer callback: " + str(e))

            self._prev_id = model.register_observer(prev_layer,
                                                    compute_stats_prev)

    def __del__(self):
        if self._model() is not None:
            self._model().unregister_observer(self._id)
            if self._prev_layer is not None:
                self._model().unregister_observer(self._prev_id)

    def __repr__(self):
        data = "{layer: " + self._layer.name + ", layer_type: " + \
            str(self._layer.parameters.layer_type).split(".")[-1]
        if self._prev_layer is not None:
            data += ", input_sparsity: " + format(self.input_sparsity, ".2f")
        data += ", output_sparsity: " + format(self.output_sparsity, ".2f")
        if self._prev_layer is not None:
            data += ", ops: " + format(self.ops, ".0f")
        data += "}"
        return data

    def __str__(self):

        def str_column_data(data, col_width=20):
            if len(data) > col_width - 1:
                formatted_data = data[:col_width - 1] + ' '
            else:
                formatted_data = data + ' ' * (col_width - len(data))

            return formatted_data

        data = str_column_data("Layer (type)", 30)
        if self._prev_layer is not None:
            data += str_column_data("input sparsity")
        data += str_column_data("output sparsity")
        if self._prev_layer is not None:
            data += str_column_data("ops")

        data += "\n"
        layer_type = str(self._layer.parameters.layer_type).split(".")[-1]
        data += str_column_data(f"{self._layer.name} ({layer_type})", 30)
        if self._prev_layer is not None:
            data += str_column_data(format(self.input_sparsity, ".2f"))
        data += str_column_data(format(self.output_sparsity, ".2f"))
        if self._prev_layer is not None:
            data += str_column_data(format(self.ops, ".0f"))

        return data

    @property
    def ops(self):
        """Get average number of inference operations per sample.

        Returns:
            int: the number of operations per sample.

        """
        ops_per_event = 0
        layer_params = self._layer.parameters
        if layer_params.layer_type == LayerType.Convolutional:
            ops_per_event = (layer_params.kernel_width *
                             layer_params.kernel_height *
                             layer_params.num_neurons)
        elif layer_params.layer_type == LayerType.SeparableConvolutional:
            ops_dw = layer_params.kernel_width * layer_params.kernel_height
            # Assume we process every potential increment as an event
            spikes_dw = ops_dw
            ops_pw = spikes_dw * layer_params.num_neurons
            ops_per_event = ops_dw + ops_pw
        elif layer_params.layer_type == LayerType.FullyConnected:
            ops_per_event = layer_params.num_neurons
        else:
            raise TypeError("Exception in LayerStatistics: ops property is not "
                            "available for " + str(layer_params.layer_type))
        if self._prev_layer is None:
            return ops_per_event
        else:
            return (ops_per_event * np.prod(self._layer.input_dims) *
                    (1 - self.input_sparsity))

    @property
    def possible_spikes(self):
        """Get possible spikes for the layer.

        Returns:
            int: the possible spike amount value.

        """
        return np.prod(self._layer.output_dims)

    @property
    def row_sparsity(self):
        """Get kernel row sparsity.

        Compute row sparsity for kernel weights.

        Returns:
          float: the kernel row sparsity value.

        """
        if (self._layer.parameters.layer_type == LayerType.Convolutional or
                self._layer.parameters.layer_type
                == LayerType.SeparableConvolutional):
            row_sparsity = 0.0
            weights = self._layer.get_variable("weights")
            wshape = weights.shape
            if np.prod(wshape) == 0:
                raise ValueError("Exception in LayerStatistics: weights shape "
                                 "have null dimension: " + str(wshape))

            # Going through all line blocks
            for f in range(wshape[3]):
                for c in range(wshape[2]):
                    for y in range(wshape[1]):
                        if np.array_equal(weights[:, y, c, f],
                                          np.zeros((wshape[0]))):
                            # Counting when line block is full of zero.
                            row_sparsity += 1
            return row_sparsity / (wshape[1] * wshape[2] * wshape[3])
        else:
            return None

    @property
    def input_sparsity(self):
        """Get average input sparsity for the layer.

        Returns:
            float: the average sparsity value.

        """
        return 0 if self._spiking_loop == 0 else (self._input_sparsity /
                                                  self._spiking_loop)

    @property
    def output_sparsity(self):
        """Get average output sparsity for the layer.

        Returns:
            float: the average output sparsity value.

        """
        return 0 if self._spiking_loop == 0 else (self._output_sparsity /
                                                  self._spiking_loop)

    @property
    def layer_name(self):
        """Get the name of the corresponding layer.

        Returns:
            str: the layer name.

        """
        return self._layer.name
