from six.moves.urllib_parse import urlencode
import trafaret as t

from datarobot import enums
from .api_object import APIObject
from ..utils import encode_utf8_if_py2, from_api, parse_time, raw_prediction_response_to_dataframe

_base_metadata_path = 'projects/{project_id}/predictionsMetadata/'
_get_metadata_path = _base_metadata_path + '{prediction_id}/'
# get predictions for particular prediction id.
_get_path = 'projects/{project_id}/predictions/{prediction_id}/'


class Predictions(APIObject):
    """
    Represents predictions metadata and provides access to prediction results.

    Attributes
    ----------
    project_id : str
        id of the project the model belongs to
    model_id : str
        id of the model
    prediction_id : str
        id of generated predictions
    includes_prediction_intervals : bool, optional
        (New in v2.16) For :ref:`time series <time_series>` projects only.
        Indicates if prediction intervals will be part of the response. Defaults to False.
    prediction_intervals_size : int, optional
        (New in v2.16) For :ref:`time series <time_series>` projects only.
        Indicates the percentile used for prediction intervals calculation. Will be present only
        if `includes_prediction_intervals` is True.
    forecast_point : datetime.datetime, optional
        (New in v2.20) For :ref:`time series <time_series>` projects only. This is the default point
        relative to which predictions will be generated, based on the forecast window of the
        project. See the time series :ref:`prediction documentation <time_series_predict>` for more
        information.
    predictions_start_date : datetime.datetime or None, optional
        (New in v2.20) For :ref:`time series <time_series>` projects only. The start date for bulk
        predictions. Note that this parameter is for generating historical predictions using the
        training data. This parameter should be provided in conjunction with
        ``predictions_end_date``. Can't be provided with the ``forecast_point`` parameter.
    predictions_end_date : datetime.datetime or None, optional
        (New in v2.20) For :ref:`time series <time_series>` projects only. The end date for bulk
        predictions, exclusive. Note that this parameter is for generating historical predictions
        using the training data. This parameter should be provided in conjunction with
        ``predictions_start_date``. Can't be provided with the ``forecast_point`` parameter.

    Examples
    --------

    List all predictions for a project

    .. code-block:: python

        import datarobot as dr

        # Fetch all predictions for a project
        all_predictions = dr.Predictions.list(project_id)

        # Inspect all calculated predictions
        for predictions in all_predictions:
            print(predictions)  # repr includes project_id, model_id, and dataset_id

    Retrieve predictions by id

    .. code-block:: python

        import datarobot as dr

        # Getting predictions by id
        predictions = dr.Predictions.get(project_id, prediction_id)

        # Dump actual predictions
        df = predictions.get_all_as_dataframe()
        print(df)
    """

    def __init__(self, project_id, prediction_id, model_id=None, dataset_id=None,
                 includes_prediction_intervals=None, prediction_intervals_size=None,
                 forecast_point=None, predictions_start_date=None, predictions_end_date=None):
        self.project_id = project_id
        self.model_id = model_id
        self.dataset_id = dataset_id
        self.prediction_id = prediction_id
        self.path = _get_path.format(project_id=self.project_id,
                                     prediction_id=self.prediction_id)
        self.includes_prediction_intervals = includes_prediction_intervals
        self.prediction_intervals_size = prediction_intervals_size
        self.forecast_point = forecast_point
        self.predictions_start_date = predictions_start_date
        self.predictions_end_date = predictions_end_date

    _metadata_trafaret = t.Dict({
        t.Key('id'): t.String(),
        t.Key('url'): t.String(),
        t.Key('model_id'): t.String(),
        t.Key('prediction_dataset_id'): t.String(),
        t.Key('includes_prediction_intervals'): t.Bool(),
        t.Key('prediction_intervals_size', optional=True): t.Int(),
        t.Key('forecast_point', optional=True): parse_time,
        t.Key('predictions_start_date', optional=True): parse_time,
        t.Key('predictions_end_date', optional=True): parse_time,
    }).ignore_extra('*')

    @classmethod
    def _build_list_path(cls, project_id, model_id=None, dataset_id=None):
        args = {}
        if model_id:
            args['modelId'] = model_id
        if dataset_id:
            args['predictionDatasetId'] = dataset_id

        path = _base_metadata_path.format(project_id=project_id)
        if args:
            path = '{}?{}'.format(path, urlencode(args))

        return path

    @classmethod
    def _from_server_object(cls, project_id, item):
        pred = cls(
            project_id,
            prediction_id=item['id'],
            model_id=item['model_id'],
            dataset_id=item.get('prediction_dataset_id') or item.get('dataset_id'),
            includes_prediction_intervals=item['includes_prediction_intervals']
        )
        if pred.includes_prediction_intervals:
            pred.prediction_intervals_size = item['prediction_intervals_size']
        if item.get('forecast_point'):
            pred.forecast_point = item['forecast_point']
        if item.get('predictions_start_date'):
            pred.predictions_start_date = item['predictions_start_date']
        if item.get('predictions_end_date'):
            pred.predictions_end_date = item['predictions_end_date']

        return pred

    @classmethod
    def list(cls, project_id, model_id=None, dataset_id=None):
        """
        Fetch all the computed predictions metadata for a project.

        Parameters
        ----------
        project_id : str
            id of the project
        model_id : str, optional
            if specified, only predictions metadata for this model will be retrieved
        dataset_id : str, optional
            if specified, only predictions metadata for this dataset will be retrieved

        Returns
        -------
        A list of :py:class:`Predictions <datarobot.models.Predictions>` objects
        """
        path = cls._build_list_path(project_id, model_id=model_id, dataset_id=dataset_id)
        converted = from_api(cls._server_data(path))
        retval = []
        for item in converted['data']:
            validated = cls._metadata_trafaret.check(item)
            pred = cls._from_server_object(project_id, validated)
            retval.append(pred)
        return retval

    @classmethod
    def get(cls, project_id, prediction_id):
        """
        Retrieve the specific predictions metadata

        Parameters
        ----------
        project_id : str
            id of the project the model belongs to
        prediction_id : str
            id of the prediction set

        Returns
        -------
        :py:class:`Predictions <datarobot.models.Predictions>` object representing specified
        predictions
        """
        path = _get_metadata_path.format(project_id=project_id,
                                         prediction_id=prediction_id)

        converted = from_api(cls._server_data(path))
        validated = cls._metadata_trafaret.check(converted)

        return cls._from_server_object(project_id, validated)

    def get_all_as_dataframe(self, class_prefix=enums.PREDICTION_PREFIX.DEFAULT):
        """
        Retrieve all prediction rows and return them as a pandas.DataFrame.

        Parameters
        ----------
        class_prefix : str, optional
            The prefix to append to labels in the final dataframe. Default is ``class_``
            (e.g., apple -> class_apple)

        Returns
        -------
        dataframe: pandas.DataFrame
        """
        data = self._server_data(self.path)
        return raw_prediction_response_to_dataframe(data, class_prefix)

    def download_to_csv(self, filename, encoding='utf-8'):
        """
        Save prediction rows into CSV file.

        Parameters
        ----------
        filename : str or file object
            path or file object to save prediction rows
        encoding : string, optional
            A string representing the encoding to use in the output file, defaults to
            'utf-8'
        """
        df = self.get_all_as_dataframe()
        df.to_csv(
            path_or_buf=filename,
            header=True,
            index=False,
            encoding=encoding,
        )

    def __repr__(self):
        template = u'{}(prediction_id={!r}, project_id={!r}, model_id={!r}, dataset_id={!r}, ' \
                   u'includes_prediction_intervals={!r}, prediction_intervals_size={!r}, ' \
                   u'forecast_point={!r}, predictions_start_date={!r}, predictions_end_date={!r})'
        return encode_utf8_if_py2(template.format(
            type(self).__name__,
            self.prediction_id,
            self.project_id,
            self.model_id,
            self.dataset_id,
            self.includes_prediction_intervals,
            self.prediction_intervals_size,
            self.forecast_point,
            self.predictions_start_date,
            self.predictions_end_date,
        ))
