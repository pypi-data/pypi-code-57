import numpy
import bytegain.custom.model_data.row_handler as row_handler
import xgboost


class ProdXgbClassifier(object):
    def __init__(self, model_spec):
        self._row_handler = row_handler.RowHandler(load_from=model_spec.get_row_handler_file())
        self._bst = xgboost.Booster(model_file = model_spec.get_model_file())
        print("Model %s fields: %s" % (model_spec._model_name, str(self._row_handler.get_fields())))

    def get_fields(self):
        return self._row_handler.get_fields()

    def classify(self, row_dict):
        # Create 1xM input array
        vec = numpy.asarray([self._row_handler.get_data_from_row(row_dict)])
        vec = xgboost.DMatrix(vec)

        predict = self._bst.predict(vec)
        # Return the positive possibility as a native float
        return float(predict[0])

    def classify_batch(self, batch):
        if batch:
            rows = [self._row_handler.get_data_from_row(x) for x in batch]
            vec = numpy.asarray(rows)
            vec = xgboost.DMatrix(vec)
            predicts = self._bst.predict(vec)
            return [float(x) for x in predicts]
        else:
            return [] # prevent blowup on no rows
