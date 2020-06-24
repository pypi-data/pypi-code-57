import numpy as np
from abc import ABCMeta, abstractmethod
from skimage import filters, transform
# ToDo: cache input for non reversible formatters to make them reversible


class NotReversibleError(NotImplementedError):
    pass


class ImageFormatter(metaclass=ABCMeta):
    DEFAULT_PARAMS = {}

    def __init__(self, **kw):
        self.parameters = self.DEFAULT_PARAMS.copy()
        self.parameters.update(kw)

    @property
    @abstractmethod
    def input_dim(self): return 4

    @property
    @abstractmethod
    def output_dim(self): return 4

    @abstractmethod
    def apply(self, data):
        '''Apply the format.

        Arguments:
        data: numpy array containing the data

        Returns: numpy array of formatted data
        '''

    @abstractmethod
    def revert(self, data):
        '''Revert the formatting.

        Arguments:
        data: numpy array containing the formatted data

        Returns: numpy array of data that is similar to the original data (i.e. has the same shape)
        '''

    @abstractmethod
    def get_output_shape(self, input_shape):
        '''Calculate shape of the data after formatting.

        Arguments:
        input_shape: tuple/list describing the original shape

        Returns: tuple describing the respective output shape
        '''

    @abstractmethod
    def get_revert_output_shape(self, output_shape):
        '''Calculate shape of the data after reverse formatting.

        Arguments:
        output_shape: tuple/list describing the original shape

        Returns: tuple describing the respective output shape
        '''


class FormattingPipeline(ImageFormatter):
    @property
    def input_dim(self):
        dim = None
        for formatter in self.formatter_list:
            dim = formatter.input_dim
            if dim is not None:
                break
        return dim

    @property
    def output_dim(self):
        dim = None
        for formatter in reversed(self.formatter_list):
            dim = formatter.output_dim
            if dim is not None:
                break
        return dim

    def __init__(self, formatter_list):
        dim = None
        for formatter in formatter_list:
            assert isinstance(
                formatter, ImageFormatter), "All formatters in the formatter list must be subclasses of ImageFormatter."
            if dim is not None and formatter.input_dim is not None:
                assert formatter.input_dim == dim, 'Input dimension mismatch. Formatter {} expects {} input dimensions but got {}.'.format(
                    type(formatter).__name__, formatter.input_dim, dim)
            if formatter.output_dim is not None:
                dim = formatter.output_dim
        self.formatter_list = formatter_list

    def apply(self, data):
        for formatter in self.formatter_list:
            data = formatter.apply(data)
        return data

    def revert(self, data):
        for formatter in reversed(self.formatter_list):
            data = formatter.revert(data)
        return data

    def get_output_shape(self, input_shape):
        for formatter in self.formatter_list:
            input_shape = formatter.get_output_shape(input_shape)
        return input_shape

    def get_revert_output_shape(self, output_shape):
        for formatter in reversed(self.formatter_list):
            output_shape = formatter.get_revert_output_shape(output_shape)
        return output_shape


class EmptyFormatter(ImageFormatter):
    '''A formatter that does not change the data'''

    @property
    def input_dim(self): return None

    @property
    def output_dim(self): return None

    def apply(self, data): return data

    def revert(self, data): return data

    def get_output_shape(self, input_shape): return input_shape

    def get_revert_output_shape(self, output_shape): return output_shape


class StackProjector(ImageFormatter):
    '''Project a stack onto a single plane.

    Works with any numpy method that reduces a given axis. For example: amin, amax, median, std
    '''
    DEFAULT_PARAMS = {'function': np.median}

    @property
    def input_dim(self): return 4

    @property
    def output_dim(self): return 3

    def apply(self, data):
        """Apply numpy function to data"""
        return self.parameters['function'](data, axis=0)

    def revert(self, data):
        raise NotReversibleError

    def get_output_shape(self, input_shape):
        return input_shape[1:]

    def get_revert_output_shape(self, output_shape):
        raise NotReversibleError


class StackGaussianBlur(ImageFormatter):
    '''Apply a gaussian blur to every plane of a stack.

    Expects the first axis to be the time axis and the second and third to be x and y.'''

    DEFAULT_PARAMS = {'sigma': 1}

    @property
    def input_dim(self): return None

    @property
    def output_dim(self): return None

    def apply(self, data):
        """Apply gaussian filter to each xy plane in data"""
        sigma = [0] * data.ndim
        sigma[1:3] = [self.parameters['sigma']] * 2
        return filters.gaussian(data, sigma=sigma)

    def revert(self, data):
        raise NotReversibleError

    def get_output_shape(self, input_shape):
        return input_shape

    def get_revert_output_shape(self, output_shape):
        raise NotReversibleError


class StackSubtractBackground(ImageFormatter):
    '''Top Hat background subtraction with disk or ball.

    Expects the first axis to be the time axis and the second and third to be x and y.
    Data is converted to uint8. It is recommended to apply normalization with clipping enabled
    before and after background subtraction (using a filter pipeline).
    '''
    DEFAULT_PARAMS = {'radius': 5, 'light_background': False}

    @property
    def input_dim(self): return 4

    @property
    def output_dim(self): return 4

    def apply(self, data):
        from skimage.morphology import white_tophat, black_tophat, disk, ball
        self.cache = np.copy(data)  # cache the input in case we need to revert later
        str_el = disk(self.parameters['radius'])
        if self.parameters['light_background']:
            fun = black_tophat
        else:
            fun = white_tophat
        for n in range(data.shape[0]):
            data[n, :, :, 0] = fun(data[n, :, :, 0], str_el)
        return data

    def revert(self, data):
        try:
            return self.cache
        except AttributeError:
            raise NotReversibleError(
                'No cached data found. Use the same object for applying and reverting the formatter.')

    def get_output_shape(self, input_shape): return input_shape

    def get_revert_output_shape(self, output_shape): return output_shape


class StackNormalizer(ImageFormatter):
    '''Normalize pixel values such that most values are between 0 and 1
    inspired by https://github.com/CSBDeep/CSBDeep/blob/master/csbdeep/utils/utils.py
    '''
    DEFAULT_PARAMS = {'pmin': 1, 'pmax': 99.8, 'axis': None, 'clip': False, 'eps': 1e-20, 'dtype': np.float32}

    @property
    def input_dim(self): return None

    @property
    def output_dim(self): return None

    def apply(self, data):
        """Percentile-based image normalization."""
        self._calc_norm_mi_ma(data)
        return self._normalize_mi_ma(data)

    def revert(self, data):
        return ((self.ma - self.mi + self.parameters['eps']) * data + self.mi).astype(self.parameters['dtype'], copy=False)

    def get_output_shape(self, input_shape): return input_shape

    def get_revert_output_shape(self, output_shape): return output_shape

    def _calc_norm_mi_ma(self, data):
        self.mi = np.percentile(data, self.parameters['pmin'], axis=self.parameters['axis'], keepdims=True)
        self.ma = np.percentile(data, self.parameters['pmax'], axis=self.parameters['axis'], keepdims=True)
        if self.parameters['dtype'] is not None:
            data = data.astype(self.parameters['dtype'], copy=False)
            self.mi = self.parameters['dtype'](self.mi) if np.isscalar(
                self.mi) else self.mi.astype(self.parameters['dtype'], copy=False)
            self.ma = self.parameters['dtype'](self.ma) if np.isscalar(
                self.ma) else self.ma.astype(self.parameters['dtype'], copy=False)

    def _normalize_mi_ma(self, data):
        try:
            import numexpr
            mi = self.mi  # pylint: disable=unused-variable
            ma = self.ma  # pylint: disable=unused-variable
            eps = self.parameters['eps']  # pylint: disable=unused-variable
            data = numexpr.evaluate(
                "(data - mi) / ( ma - mi + eps )")
        except ImportError:
            data = (data - self.mi) / (self.ma - self.mi + self.parameters['eps'])
        if self.parameters['clip']:
            data = np.clip(data, 0, 1)
        return data


class StackTiler(ImageFormatter):
    '''Cut/assemble a stack into/from several (overlapping) spatial (2nd and third axis) tiles'''
    DEFAULT_PARAMS = {'tile_num': 4, 'tile_padding': (6, 6), 'tile_rows': None, 'tile_cols': None}

    def __init__(self, **kw):
        super().__init__(**kw)
        self._calc_rows_cols_tiles()

    @property
    def input_dim(self): return 4

    @property
    def output_dim(self): return 4

    def apply(self, data):
        shape = data.shape
        assert len(
            shape) == 4, 'stack must have four dimensions (time, x, y, color channels). The current stack has shape {}'.format(shape)
        assert shape[2] % self.parameters['tile_rows'] == 0, 'stack with {} pixels in y cannot be split into {} rows'.format(
            shape[2], self.parameters['tile_rows'])
        assert shape[1] % self.parameters['tile_cols'] == 0, 'stack with {} pixels in xy cannot be split into {} columns'.format(
            shape[2], self.parameters['tile_cols'])

        output_shape = self.get_output_shape(shape)
        output = np.zeros(output_shape)
        data = np.pad(data, ((0, 0), (self.parameters['tile_padding'][0], self.parameters['tile_padding'][0]),
                             (self.parameters['tile_padding'][1], self.parameters['tile_padding'][1]), (0, 0)), 'constant')
        tile = 0
        for r in range(self.parameters['tile_rows']):
            r_f = r * (output_shape[1] - 2 * self.parameters['tile_padding'][0])
            r_t = r_f + output_shape[1]
            for c in range(self.parameters['tile_cols']):
                t_f = tile * shape[0]
                t_t = t_f + shape[0]
                c_f = c * (output_shape[2] - 2 * self.parameters['tile_padding'][1])
                c_t = c_f + output_shape[2]
                output[t_f:t_t, :, :, :] = data[:, r_f:r_t, c_f: c_t, :]
                tile += 1
        return output

    def revert(self, data):
        assert data.shape[0] % self.parameters['tile_num'] == 0, 'image cannot be assembled from %r tiles.' % self.parameters['tile_num']
        num_frames = int(data.shape[0] / self.parameters['tile_num'])
        no_padding = np.array(data.shape[1:3]) - 2 * np.array(self.parameters['tile_padding'])
        output = np.zeros(self.get_revert_output_shape(data.shape))
        start_x, start_y = self.parameters['tile_padding']
        end_x = self.parameters['tile_padding'][0] + no_padding[0]
        end_y = self.parameters['tile_padding'][1] + no_padding[1]
        tile = 0
        for r in range(self.parameters['tile_rows']):
            r_f = r * no_padding[0]
            r_t = r_f + no_padding[0]
            for c in range(self.parameters['tile_cols']):
                c_f = c * no_padding[1]
                c_t = c_f + no_padding[1]
                t_f = tile * num_frames
                t_t = t_f + num_frames
                output[:, r_f:r_t, c_f:c_t, :] = data[t_f:t_t, start_x:end_x, start_y:end_y, :]
                tile += 1
        return output

    def get_output_shape(self, shape):
        new_hw = (np.divide(shape[1:3], [self.parameters['tile_rows'], self.parameters['tile_cols']]
                            ) + 2 * np.array(self.parameters['tile_padding'])).astype('uint32')
        return (shape[0] * self.parameters['tile_num'],) + tuple(new_hw) + shape[3:]

    def get_revert_output_shape(self, shape):
        new_hw = ((np.array(shape[1:3]) - 2 * np.array(self.parameters['tile_padding'])) *
                  np.array([self.parameters['tile_rows'], self.parameters['tile_cols']])).astype('uint32')
        return (shape[0] // self.parameters['tile_num'],) + tuple(new_hw) + shape[3:]

    def _calc_rows_cols_tiles(self):
        if self.parameters['tile_rows'] is None:
            self.parameters['tile_rows'] = np.sqrt(self.parameters['tile_num']).astype('uint32')
            assert (self.parameters['tile_num'] % self.parameters['tile_rows']
                    ) == 0, 'stack/image cannot be split into %r tiles.' % self.parameters['tile_num']
        if self.parameters['tile_cols'] is None:
            self.parameters['tile_cols'] = self.parameters['tile_num'] // self.parameters['tile_rows']
        self.parameters['tile_num'] = self.parameters['tile_rows'] * self.parameters['tile_cols']


class PerformanceTiler(StackTiler):
    '''Tile an input array such that the number of planes is close to a multiple of the number of CPUs.'''
    DEFAULT_PARAMS = {'tile_padding': (0, 0), 'separate_stacks': False}

    @property
    def output_dim(self):
        if self.parameters['separate_stacks']:
            return 5
        else:
            return 4

    def apply(self, data):
        self._calc_rows_cols_tiles(data.shape)
        if self.parameters['separate_stacks']:
            self.parameters['tile_padding'] = (0, 0)
            return np.concatenate(np.split(np.array(np.split(data, self.parameters['tile_rows'], axis=1)), self.parameters['tile_cols'], axis=3))
        else:
            return super().apply(data)

    def revert(self, data):
        if self.estimated_parameters:
            raise NotImplementedError(
                'Cannot reliably revert PerformanceTiler before it has been applied to actual data, because the parameters may change depending on the data.')
        if self.parameters['separate_stacks']:
            return np.concatenate(np.concatenate(np.array(np.split(data, self.parameters['tile_cols'])), axis=3), axis=1)
        else:
            return super().revert(data)

    def get_output_shape(self, shape):
        temp_parm = self.parameters.copy()  # only apply() should permanently change parameters, therefore we cache the parameters
        if self.parameters['separate_stacks']:
            self.parameters['tile_padding'] = (0, 0)
        self._calc_rows_cols_tiles(shape)
        result = super().get_output_shape(shape)
        self.parameters = temp_parm  # restore parameters
        if self.parameters['separate_stacks']:
            result = (self.parameters['tile_num'], round(result[0] / self.parameters['tile_num'])) + result[1:]
        return result

    def get_revert_output_shape(self, shape):
        if self.estimated_parameters:
            raise NotImplementedError(
                'Cannot reliably calculate revert output shape before PerformanceTiler has been applied to actual data, because the parameters may change depending on the data.')
        return super().get_revert_output_shape(shape)

    def _calc_rows_cols_tiles(self, shape=None):
        '''guess the best number of rows and cols to match the number of cpus.

        If the shape of the data is given, we take it into account.
        Note that this means the actual parameters of PerformanceTiler depend on the data.
        '''

        import math
        import multiprocessing as mp
        ncpu = mp.cpu_count()
        root = math.sqrt(ncpu)
        smaller = math.floor(root)
        larger = math.ceil(root)
        last_round = (smaller * larger) % ncpu
        # the last computing round should have less than half of all cores idle
        if last_round > 0 and last_round < ncpu / 2:
            larger -= 1
        self.parameters['tile_num'] = smaller * larger
        self.parameters['tile_rows'] = smaller
        self.parameters['tile_cols'] = larger
        self.estimated_parameters = True
        if shape is not None:
            # adapt the parameters to the shape of the data
            if shape[1] > shape[2]:
                # cut more frequently along the longer axis
                self.parameters['tile_rows'] = larger
                self.parameters['tile_cols'] = smaller
            # make sure, padding does not eat up our performance gain
            overhead = self._tiling_overhead(shape)
            while overhead > ncpu/1.5:
                self.parameters['tile_cols'] -= 1
                overhead = self._tiling_overhead(shape)
            if self.parameters['tile_cols'] <= 1:
                self.parameters['tile_cols'] = 1
                self.parameters['tile_padding'] = (self.parameters['tile_padding'][0], 0)
            while overhead > ncpu/1.5:
                self.parameters['tile_rows'] -= 1
                overhead = self._tiling_overhead(shape)
            if self.parameters['tile_rows'] <= 1:
                self.parameters['tile_rows'] = 1
                self.parameters['tile_padding'] = (0, self.parameters['tile_padding'][1])
            # make sure the image is divisible by our chosen number of rows and cols:
            while shape[1] % self.parameters['tile_rows'] > 0:
                self.parameters['tile_rows'] -= 1
            while shape[2] % self.parameters['tile_cols'] > 0:
                self.parameters['tile_cols'] -= 1
            self.parameters['tile_num'] = self.parameters['tile_rows'] * self.parameters['tile_cols']
            self.estimated_parameters = False

    def _tiling_overhead(self, shape):
        row_overhead = self.parameters['tile_rows'] * self.parameters['tile_padding'][0] * 2
        col_overhead = self.parameters['tile_cols'] * self.parameters['tile_padding'][1] * 2
        return (row_overhead + col_overhead) / (shape[1] * shape[2])


class ParallelFlattener(ImageFormatter):
    '''Split a stack into tiles and perform the given function on each tile in parallel using multiprocessing

    Beware: Never benchmark in debugging mode! In debugging mode the memory consumption and overhead can be very severe.
    '''
    DEFAULT_PARAMS = {'function': np.median, 'args': (), 'kw': {'axis': 0}}

    @property
    def input_dim(self): return 4

    @property
    def output_dim(self): return 3

    def apply(self, data):
        import multiprocessing as mp
        formatter = PerformanceTiler(separate_stacks=True)
        data = formatter.apply(data)
        pool = mp.Pool(mp.cpu_count())
        global _results  # results need to be global so that multiprocessing can access them
        _results = []  # make sure we start with an empty list as results
        for tile in range(data.shape[0]):
            pool.apply_async(_apply_fun, args=(data[tile, :, :, :], tile, self.parameters), callback=_collect_result)
        pool.close()
        pool.join()
        _results.sort(key=lambda x: x[1])
        res = np.array([r[0] for r in _results])
        _results = []
        return np.concatenate(np.concatenate(np.array(np.split(res, formatter.parameters['tile_cols'])), axis=2), axis=0)

    def revert(self, data):
        raise NotImplementedError('Cannot revert flattening of stacks')

    def get_output_shape(self, shape):
        return shape[1:]

    def get_revert_output_shape(self, shape):
        raise NotImplementedError('Cannot revert flattening of stacks')


#################################
'''Global functions and variable required for StackSubtractBackgroundParallel.'''
_results = []


def _collect_result(result):
    global _results
    _results.append(result)


def _apply_fun(stack, i, parameters):
    flat = parameters['function'](stack, *parameters['args'], **parameters['kw'])
    return flat, i
#################################


class StackSlicer(ImageFormatter):
    '''Slice stack into several overlapping pieces along the first (time) axis.'''
    DEFAULT_PARAMS = {'slice_len': 10, 'slice_padding': 2}

    @property
    def input_dim(self): return 4

    @property
    def output_dim(self): return 5

    def apply(self, data):
        split_ind = np.array(range(0, data.shape[0], self.parameters['slice_len']))
        data = np.array_split(data, split_ind[1:])
        if self.parameters['slice_padding'] > 0:
            output = np.zeros((len(data), self.parameters['slice_len'] +
                               self.parameters['slice_padding']) + data[0].shape[1:])
            for s in range(len(data)):
                if s == 0:
                    output[s] = np.insert(data[s], 0, data[s][0:self.parameters['slice_padding']], axis=0)
                else:
                    try:
                        output[s] = np.insert(data[s], 0, data[s-1][-self.parameters['slice_padding']:], axis=0)
                    except ValueError:
                        raw = np.insert(data[s], 0, data[s-1][-self.parameters['slice_padding']:], axis=0)
                        output[s] = self._pad(raw, output[s].shape[0])
            data = output
        else:
            if data[0].shape[0] != data[-1].shape[0]:
                data[-1] = self._pad(data[-1], data[0].shape[0])
            data = np.array(data)
        return data

    def revert(self, data):
        output = np.zeros((data.shape[0], data.shape[1] - self.parameters['slice_padding']) + data.shape[2:])
        for s in range(data.shape[0]):
            output[s, :] = data[s, self.parameters['slice_padding']:]
        return np.concatenate(output, axis=0)

    def get_output_shape(self, shape):
        return (int(np.ceil(shape[0] / self.parameters['slice_len'])), self.parameters['slice_len'] + self.parameters['slice_padding']) + shape[1:]

    def get_revert_output_shape(self, shape):
        return (shape[0] * (shape[1] - self.parameters['slice_padding']),) + shape[2:]

    @staticmethod
    def _pad(raw, target_len):
        missing = target_len - raw.shape[0]
        padding = np.zeros((missing,) + raw.shape[1:])
        return np.concatenate([raw, padding])


class StackScaler(ImageFormatter):
    '''Scale stacks in the x-y plane'''
    DEFAULT_PARAMS = {'scale_factor': None, 'target_dim': None}

    @property
    def input_dim(self): return None

    @property
    def output_dim(self): return None

    def apply(self, data):
        self.orig_shape = data.shape
        return transform.resize(data, self.get_output_shape(self.orig_shape), anti_aliasing=True)

    def revert(self, data):
        try:
            return transform.resize(data, self.orig_shape, anti_aliasing=True)
        except AttributeError:
            raise NotReversibleError('Need to apply stack scaler before it can be reversed')

    def get_output_shape(self, input_shape):
        if self.parameters['target_dim'] is not None:
            try:
                x = self.parameters['target_dim'][0]
                y = self.parameters['target_dim'][1]
            except TypeError:
                x = self.parameters['target_dim']
                y = self.parameters['target_dim']
        else:
            try:
                x = round(input_shape[1] * self.parameters['scale_factor'][0])
                y = round(input_shape[2] * self.parameters['scale_factor'][1])
            except TypeError:
                x = round(input_shape[1] * self.parameters['scale_factor'])
                y = round(input_shape[1] * self.parameters['scale_factor'])
        return (input_shape[0], x, y) + input_shape[3:]

    def get_revert_output_shape(self, input_shape):
        try:
            return self.orig_shape
        except AttributeError:
            raise NotReversibleError('Need to apply stack scaler before it can be reversed')
