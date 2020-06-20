import json

try:
    import numpy

    has_numpy = True
except:
    has_numpy = False


class FnJSONEncoder(json.JSONEncoder):
    def default(self, obj_to_encode):
        """Pandas and Numpy have some specific types that we want to ensure
        are coerced to Python types, for JSON generation purposes. This attempts
        to do so where applicable.
        """
        # Pandas dataframes have a to_json() method, so we'll check for that and
        # return it if so.
        # This may be a little slow, but it is simple for now
        if hasattr(obj_to_encode, "to_json"):
            return json.loads(obj_to_encode.to_json(orient="records"))

        if has_numpy:
            # Numpy objects report themselves oddly in error logs, but this generic
            # type mostly captures what we're after.
            if isinstance(obj_to_encode, numpy.generic):
                return numpy.asscalar(obj_to_encode)

            # ndarray -> list, pretty straightforward.
            if isinstance(obj_to_encode, numpy.ndarray):
                return obj_to_encode.to_list()

        # If none of the above apply, we'll default back to the standard JSON encoding
        # routines and let it work normally.
        return super().default(obj_to_encode)
