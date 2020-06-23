def ndarray_to_mixed_list(obj):
    """
    Convert a multi dimensional numpy array to list of ndarray rows.
    This is as if everything is python lists except the final rows.
    """
    result = []
    # target = result
    # for dimension in obj.shape[:-1]:
    #     target.append([] * dimension)
    #     target = target[0]

    for path_tuple, row in get_numpy_ndarray_rows(obj):
        target = result
        for index in path_tuple[:-1]:
            try:
                target = target[index]
            except IndexError:
                target.append([])
                target = target[-1]
        target.append(row)

    return result



    def test_ndarray_to_mixed_list1(self):
        obj = np.array([
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8, 9], [14, 15, 16]],
        ], np.int8)
        result = ndarray_to_mixed_list(obj)

        assert isinstance(result, list)
        assert isinstance(result[0], list)
        assert np.array_equal(np.array([1, 2, 3], np.int8), result[0][0])
        assert np.array_equal(np.array([14, 15, 16], np.int8), result[1][1])




    def get_and_stabilize_item(self, parent_obj, to_obj_attr=not_found, to_obj_key=not_found):
        """
        This is used to stabilize the data types.
        The main usage is for Numpy arrays when ignore_order=True
        In such arrays, with every lookup of items inside the array,
        a new array object is returned by Numpy. That causes a lot of issues
        with DeepHash since during hashing, we use the IDs of non-hashable objects
        to track them.
        """
        if to_obj_attr is not not_found:
            obj = original_obj = getattr(parent_obj, to_obj_attr)
        elif to_obj_key is not not_found:
            obj = original_obj = parent_obj[to_obj_key]
        else:
            raise RuntimeError('to_obj_attr or to_obj_key need to be defined.')

        if self.ignore_order and isinstance(obj, np_ndarray) and len(obj.shape) > 1:
            if to_obj_attr is not not_found:
                try:
                    obj = ndarray_to_mixed_list(obj)
                    setattr(parent_obj, to_obj_attr, obj)
                except Exception as e:
                    raise type(e)(TYPE_STABILIZATION_MSG.format(original_obj, e))
            else:
                try:
                    obj = ndarray_to_mixed_list(obj)
                    parent_obj[to_obj_key] = obj
                except Exception as e:
                    raise type(e)(TYPE_STABILIZATION_MSG.format(original_obj, e))
        return obj
