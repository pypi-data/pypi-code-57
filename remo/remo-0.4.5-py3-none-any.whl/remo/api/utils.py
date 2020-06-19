# import copy
# import itertools
#
# import wrapt
#
#
# class SliceableGenerator(wrapt.ObjectProxy):
#     """
#     Wrapper class intended to be able to apply slice and indexation over
#     iterable, particularly generators
#     """
#     __slots__ = ('_size',)
#
#     def __init__(self, iterable, size=None):
#         """
#         :param iterable:
#         :param size: Optional size of generator
#         """
#         super().__init__(iterable)
#         self._self_size = size
#
#     def __getitem__(self, item):
#         iterable = self.__wrapped__
#         if isinstance(item, slice):
#             return itertools.islice(iterable, item.start, item.stop, item.step)
#         elif isinstance(item, int):
#             if item < 0:
#                 raise IndexError('indices must be non-negative number')
#
#             elem = list(itertools.islice(iterable, item, item + 1))
#             if elem:
#                 return elem[0]
#             else:
#                 raise IndexError('generator index out of range')
#         else:
#             raise TypeError(
#                 'list indices must be integers or slices, not {}'.format(item.__class__.__name__)
#             )
#
#     def __len__(self):
#         return self._self_size if self._self_size is not None else len(self.__wrapped__)
#
#     def __copy__(self):
#         return copy.copy(self.__wrapped__)
#
#     def __deepcopy__(self, memodict={}):
#         return copy.deepcopy(self.__wrapped__)
