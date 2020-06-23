"Datasets module of official Python client for Driverless AI." ""

import ast
import re
import tempfile
import time
from typing import Any, Dict, Iterable, List, TYPE_CHECKING, Union

from driverlessai import _core
from driverlessai import _recipes
from driverlessai import _utils


if TYPE_CHECKING:
    import pandas  # noqa F401


class Connectors:
    """Interact with data sources that are enabled on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> List[str]:
        """Return list of data sources enabled on the Driverless AI server."""
        return self._client._backend.list_allowed_file_systems(0, None)


class DataPreviewJob(_utils.ServerJob):
    """Monitor generation of a data preview on the Driverless AI server.

    Attributes:
        key: unique ID
    """

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._info = self._client._backend.get_data_preview_job(self.key)

    def result(self, silent: bool = False) -> "DataPreviewJob":
        """Wait for job to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def status(self, verbose: int = None) -> str:
        """Return short job status description string."""
        return self._status().message


class Dataset:
    """Interact with a dataset on the Driverless AI server.

    Attributes:
        columns (List[str]): list of column names
        data_source (str): original source of data
        file_path (str): path to dataset bin file on the server
        key (str): unique ID
        name (str): display name
        shape (Tuple[int, int]): dimensions (rows, cols)
    """

    def __init__(self, client: "_core.Client", info: Any) -> None:
        self._client = client
        self._info = info
        self._logical_types = {
            "categorical": "cat",
            "date": "date",
            "datetime": "datetime",
            "id": "id",
            "numerical": "num",
            "text": "text",
        }
        self.columns = [c.name for c in info.columns]
        self.data_source = info.data_source
        self.file_path = info.bin_file_path
        self.key = info.key
        self.name = info.name
        self.shape = (info.row_count, len(info.columns))

    def __repr__(self) -> str:
        return f"{self.__class__} {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    # NOTE get_raw_data is not stable!
    def _get_data(
        self, start: int = 0, num_rows: int = None
    ) -> List[List[Union[bool, float, str]]]:
        """Retrieve data as a list.

        Args:
            start: index of first row to include
            num_rows: number of rows to include
        """
        num_rows = num_rows or self.shape[0]
        return self._client._backend.get_raw_data(self.key, start, num_rows).rows

    def _import_modified_datasets(
        self, recipe_job: _recipes.RecipeJob
    ) -> List["Dataset"]:
        data_files = recipe_job.result(silent=True)._info.entity.data_files
        keys = [self._client._backend.create_dataset_from_recipe(f) for f in data_files]
        datasets = [
            DatasetJob(self._client, key, name=key).result(silent=True) for key in keys
        ]
        return datasets

    def _update(self) -> None:
        self._info = self._client._backend.get_dataset_job(self.key).entity
        self.name = self._info.name

    def column_summaries(
        self, columns: List[str] = None
    ) -> "DatasetColumnSummaryCollection":
        """Returns a collection of column summaries.

        The collection can be indexed by number or column name:

        - ``dataset.column_summaries()[0]``
        - ``dataset.column_summaries()[0:3]``
        - ``dataset.column_summaries()['C1']``

        A column summary has the following attributes:

        - ``count``: count of non-missing values
        - ``data_type``: raw data type detected by Driverless AI
          when the data was imported
        - ``datetime_format``: user defined datetime format to be used by Driverless AI
          (see ``dataset.set_datetime_format()``)
        - ``freq``: count of most frequent value
        - ``logical_types``: list of user defined data types to be used by Driverless AI
          (overrides ``data_type``, also see ``dataset.set_logical_types()``)
        - ``max``: maximum value for numeric data
        - ``mean``: mean of values for numeric data
        - ``min``: minimum value for numeric data
        - ``missing``: count of missing values
        - ``name``: column name
        - ``sd``: standard deviation of values for numeric data
        - ``unique``: count of unique values

        Printing the collection or an individual summary displays a histogram
        along with summary information, like so::

            --- C1 ---

             4.3|███████
                |█████████████████
                |██████████
                |████████████████████
                |████████████
                |███████████████████
                |█████████████
                |████
                |████
             7.9|████

            Data Type: real
            Logical Types: ['categorical', 'numerical']
            Datetime Format:
            Count: 150
            Missing: 0
            Mean: 5.84
            SD: 0.828
            Min: 4.3
            Max: 7.9
            Unique: 35
            Freq: 10

        Args:
            columns: list of column names to include in the collection
        """
        return DatasetColumnSummaryCollection(self, columns=columns)

    def delete(self) -> None:
        """Delete dataset on Driverless AI server."""
        self._client._backend.delete_dataset(self.key)
        print("Driverless AI Server reported dataset", self, "deleted.")

    def download(self, dst_dir: str = ".", overwrite: bool = False) -> str:
        """Download dataset from Driverless AI server as a csv.

        Args:
            dst_dir: relative path to directory where csv should be saved
            overwrite: overwrite existing file
        """
        job = self._client._backend.create_csv_from_dataset(self.key)
        while _utils.is_server_job_running(
            self._client._backend.get_create_csv_job(job).status.status
        ):
            time.sleep(1)
        finished_job = self._client._backend.get_create_csv_job(job)
        if not _utils.is_server_job_complete(finished_job.status.status):
            raise RuntimeError(
                self._client._backend._format_server_error(finished_job.status.error)
            )
        # path needs to match expectation of _download
        path = re.sub("^/files/", "", finished_job.url)
        return self._client._download(path, dst_dir, overwrite)

    def head(self, num_rows: int = 5) -> _utils.Table:
        """Return headers and first n rows of dataset in a Table.

        Args:
            num_rows: number of rows to show
        """
        data = self._get_data(0, num_rows)
        return _utils.Table(data, self.columns)

    def modify_by_code(
        self, code: str, names: List[str] = None
    ) -> Dict[str, "Dataset"]:
        """Create a dictionary of new datasets from original dataset modified by
        a Python ``code`` string, that is the body of a function where:
            - there is an input variable ``X`` that represents the original dataset
              in the form of a datatable frame (dt.Frame)
            - return type is one of dt.Frame, pd.DataFrame, np.ndarray or a list
              of those

        Examples::

            # Keep first 4 columns
            new_dataset = dataset.modify_by_code(
                'return X[:, :4]', names=['new_dataset']
            )

            # Split on 4th column
            new_datasets = dataset.modify_by_code(
                'return [X[:, :4], X[:, 4:]]',
                names=['new_dataset_1', 'new_dataset_2']
            )

        The dictionary will map the dataset ``names`` to the returned element(s)
        from the Python ``code`` string.

        Args:
            code: Python code that modifies ``X``
            names: optional list of names for the new dataset(s)
        """
        status_update = _utils.StatusUpdate()
        status_update.display(
            f"{_utils.JobStatus.RUNNING.message} - Modifying '{self.name}' into "
            "new dataset(s)..."
        )
        # Add recipe to server and get path to recipe file on server
        key = self._client._backend.get_data_recipe_preview(self.key, code)
        completed_preview_job = DataPreviewJob(self._client, key).result(silent=True)
        # Modify the dataset with recipe
        key = self._client._backend.modify_dataset_by_recipe_file(
            completed_preview_job._info.dataset_key,
            completed_preview_job._info.recipe_path,
        )
        completed_recipe_job = _recipes.RecipeJob(self._client, key).result(silent=True)
        # Add the new datasets to DAI
        status_update.display(
            f"{_utils.JobStatus.RUNNING.message} - Importing datasets..."
        )
        datasets = self._import_modified_datasets(completed_recipe_job)
        for i, d in enumerate(datasets):
            d.rename(f"{i + 1}.{self.name}")
        status_update.display(_utils.JobStatus.COMPLETE.message)
        status_update.end()
        if names is not None:
            if len(set(names)) != len(datasets):
                raise ValueError(
                    "Number of unique names doesn't match number of new datasets."
                )
            for i, name in enumerate(names):
                datasets[i].rename(name)
        return {d.name: d for d in datasets}

    def modify_by_code_preview(self, code: str) -> _utils.Table:
        """Get a preview of the dataset modified by a Python ``code`` string,
        where:
            - there exists a variable ``X`` that represents the original dataset
              in the form of a datatable frame (dt.Frame)
            - return type is one of dt.Frame, pd.DataFrame, np.ndarray or a list
              of those (only first element of the list is shown in preview)

        Example::

            # Keep first 4 columns
            dataset.modify_by_code_preview('return X[:, :4]')

        Args:
            code: Python code that modifies ``X``
        """
        key = self._client._backend.get_data_recipe_preview(self.key, code)
        completed_job = DataPreviewJob(self._client, key).result()
        return _utils.Table(
            completed_job._info.entity.rows[:10], completed_job._info.entity.headers
        )

    def modify_by_recipe(
        self, recipe: str, names: List[str] = None
    ) -> Dict[str, "Dataset"]:
        """Create a dictionary of new datasets from original dataset modified by
        a recipe.

        The dictionary will map the dataset ``names`` to the returned element(s)
        from the recipe.

        Args:
            recipe: path to recipe or url for recipe
            names: optional list of names for the new dataset(s)
        """
        status_update = _utils.StatusUpdate()
        status_update.display(
            f"{_utils.JobStatus.RUNNING.message} - Modifying '{self.name}' into "
            "new dataset(s)..."
        )
        if re.match("^http[s]?://", recipe):
            key = self._client._backend.modify_dataset_by_recipe_url(self.key, recipe)
        else:
            # Add recipe file to server
            path = self._client._backend.perform_upload(recipe, skip_parse=True)[0]
            key = self._client._backend.modify_dataset_by_recipe_file(self.key, path)
        completed_recipe_job = _recipes.RecipeJob(self._client, key).result(silent=True)
        # Add the new datasets to DAI
        status_update.display(
            f"{_utils.JobStatus.RUNNING.message} - Importing datasets..."
        )
        datasets = self._import_modified_datasets(completed_recipe_job)
        for i, d in enumerate(datasets):
            d.rename(f"{i + 1}.{self.name}")
        status_update.display(_utils.JobStatus.COMPLETE.message)
        status_update.end()
        if names is not None:
            if len(set(names)) != len(datasets):
                raise ValueError(
                    "Number of unique names doesn't match number of new datasets."
                )
            for i, name in enumerate(names):
                datasets[i].rename(name)
        return {d.name: d for d in datasets}

    def rename(self, name: str) -> "Dataset":
        """Change dataset display name.

        Args:
            name: new display name
        """
        self._client._backend.update_dataset_name(self.key, name)
        self._update()
        return self

    def set_datetime_format(self, columns: Dict[str, str]) -> None:
        """Set datetime format of columns.

        Args:
            columns: dictionary where the key is the column name and
                the value is a valid datetime format
        """
        for k, v in columns.items():
            if v is None:
                v = ""
            self._client._backend.update_dataset_col_format(self.key, k, v)
        self._update()

    def set_logical_types(self, columns: Dict[str, Union[str, List[str]]]) -> None:
        """Designate columns to have the specified logical types. The logical
        type is mainly used to determine which transformers to try on the
        column's data.

        Possible logical types:

        - ``'categorical'``
        - ``'date'``
        - ``'datetime'``
        - ``'id'``
        - ``'numerical'``
        - ``'text'``

        Args:
            columns: dictionary where the key is the column name and the value
                is the logical type or a list of logical types for the column
                (to unset all logical types use a value of ``None``)

        Example::

            dataset.set_logical_types(
                {'C1': 'id', 'C2': ['categorical', 'numerical'], 'C3': None}
            )

        """
        for k, v in columns.items():
            if v is None:
                self._client._backend.update_dataset_col_logical_types(self.key, k, [])
            else:
                if isinstance(v, str):
                    v = [v]
                for lt in v:
                    if lt not in self._logical_types:
                        raise ValueError(
                            "Please use logical types from: "
                            + str(sorted(self._logical_types.keys()))
                        )
                self._client._backend.update_dataset_col_logical_types(
                    self.key, k, [self._logical_types[lt] for lt in v]
                )
        self._update()

    def split_to_train_test(
        self,
        train_size: float = 0.5,
        train_name: str = None,
        test_name: str = None,
        target_column: str = None,
        fold_column: str = None,
        time_column: str = None,
        seed: int = None,
    ) -> Dict[str, "Dataset"]:
        """Split a dataset into train/test sets on the Driverless AI server and
        return a dictionary of Dataset objects with the keys
        ``'train_dataset'`` and ``'test_dataset'``.

        Args:
            train_size: proportion of dataset rows to put in the train split
            train_name: name for the train dataset
            test_name: name for the test dataset
            target_column: use stratified sampling to create splits
            fold_column: keep rows belonging to the same group together
            time_column: split rows such that the splits are sequential with
                respect to time
            seed: random seed

        .. note:: Only one of ``target_column``, ``fold_column``, or ``time_column``
            can be passed at a time.
        """
        return self.split_to_train_test_async(
            train_size,
            train_name,
            test_name,
            target_column,
            fold_column,
            time_column,
            seed,
        ).result()

    def split_to_train_test_async(
        self,
        train_size: float = 0.5,
        train_name: str = None,
        test_name: str = None,
        target_column: str = None,
        fold_column: str = None,
        time_column: str = None,
        seed: int = None,
    ) -> "DatasetSplitJob":
        """Launch creation of a dataset train/test split on the Driverless AI
        server and return a DatasetSplitJob object to track the status.

        Args:
            train_size: proportion of dataset rows to put in the train split
            train_name: name for the train dataset
            test_name: name for the test dataset
            target_column: use stratified sampling to create splits
            fold_column: keep rows belonging to the same group together
            time_column: split rows such that the splits are sequential with
                respect to time
            seed: random seed

        .. note:: Only one of ``target_column``, ``fold_column``, or ``time_column``
            can be passed at a time.
        """
        cols = [target_column, fold_column, time_column]
        if sum([1 for x in cols if x is not None]) > 1:
            raise ValueError("Only one column argument allowed.")
        # Don't pass names here since certain file extensions in the name
        # (like .csv) cause errors, rename inside DatasetSplitJob instead
        key = self._client._backend.make_dataset_split(
            dataset_key=self.key,
            output_name1=None,
            output_name2=None,
            target=target_column,
            fold_col=fold_column,
            time_col=time_column,
            ratio=train_size,
            seed=seed,
        )
        return DatasetSplitJob(self._client, key, train_name, test_name)

    def tail(self, num_rows: int = 5) -> _utils.Table:
        """Return headers and last n rows of dataset in a Table.

        Args:
            num_rows: number of rows to show
        """
        data = self._get_data(self.shape[0] - num_rows, num_rows)
        return _utils.Table(data, self.columns)


class DatasetColumnSummary:
    """Information, statistics, and histogram for column data.

    Attributes:
        count: count of non-missing values
        data_type: raw data type detected by Driverless AI
        when the data was imported
        datetime_format: user defined datetime format to be used by Driverless AI
        (see ``dataset.set_datetime_format()``)
        freq: count of most frequent value
        logical_types: list of user defined data types to be used by Driverless AI
        (overrides ``data_type``, also see ``dataset.set_logical_types()``)
        max: maximum value for numeric data
        mean: mean of values for numeric data
        min: minimum value for numeric data
        missing: count of missing values
        name: column name
        sd: standard deviation of values for numeric data
        unique: count of unique values

    Printing a summary displays a histogram along with summary information,
    like so::

        --- C1 ---

         4.3|███████
            |█████████████████
            |██████████
            |████████████████████
            |████████████
            |███████████████████
            |█████████████
            |████
            |████
         7.9|████

        Data Type: real
        Logical Types: ['categorical', 'numerical']
        Datetime Format:
        Count: 150
        Missing: 0
        Mean: 5.84
        SD: 0.828
        Min: 4.3
        Max: 7.9
        Unique: 35
        Freq: 10

    """

    def __init__(self, column_summary: Any) -> None:
        self._hist = column_summary["hist"]
        self.count = column_summary["count"]
        self.data_type = column_summary["data_type"]
        self.datetime_format = column_summary["datetime_format"]
        self.freq = column_summary["freq"]
        self.logical_types = column_summary["logical_types"]
        self.max = column_summary["max"]
        self.mean = column_summary["mean"]
        self.min = column_summary["min"]
        self.missing = column_summary["missing"]
        self.name = column_summary["name"]
        self.sd = column_summary["std"]
        self.unique = column_summary["unique"]

    def __repr__(self) -> str:
        return f"<{self.name} Summary>"

    def __str__(self) -> str:
        s = [
            f"--- {self.name} ---\n",
            f"{self._hist}",
            f"Data Type: {self.data_type}",
            f"Logical Types: {self.logical_types!s}",
            f"Datetime Format: {self.datetime_format}",
            f"Count: {self.count!s}",
            f"Missing: {self.missing!s}",
        ]
        if self.mean not in [None, ""]:
            s.append(f"Mean: {self.mean:0.3g}")
            s.append(f"SD: {self.sd:0.3g}")
        if self.min not in [None, ""]:
            s.append(f"Min: {self.min:{'0.3g' if _utils.is_number(self.min) else ''}}")
            s.append(f"Max: {self.max:{'0.3g' if _utils.is_number(self.max) else ''}}")
        s.append(f"Unique: {self.unique!s}")
        s.append(f"Freq: {self.freq!s}")
        return "\n".join(s)


class DatasetColumnSummaryCollection:
    """Collection for storing and retrieving column summaries.

    The collection can be indexed by number or column name:

    - ``dataset.column_summaries()[0]``
    - ``dataset.column_summaries()[0:3]``
    - ``dataset.column_summaries()['C1']``

    Printing a collection displays a histogram along with summary information
    for all columns contained, like so::

        --- C1 ---

         4.3|███████
            |█████████████████
            |██████████
            |████████████████████
            |████████████
            |███████████████████
            |█████████████
            |████
            |████
         7.9|████

        Data Type: real
        Logical Types: ['categorical', 'numerical']
        Datetime Format:
        Count: 150
        Missing: 0
        Mean: 5.84
        SD: 0.828
        Min: 4.3
        Max: 7.9
        Unique: 35
        Freq: 10

    """

    def __init__(self, dataset: "Dataset", columns: List[str] = None):
        self._columns = columns or dataset.columns
        self._dataset = dataset
        self._update()

    def __getitem__(
        self, columns: Union[int, slice, str, List[str]]
    ) -> Union["DatasetColumnSummary", "DatasetColumnSummaryCollection"]:
        self._update()
        if isinstance(columns, str):
            return DatasetColumnSummary(self._column_summaries[columns])
        elif isinstance(columns, int):
            columns = self._columns[columns]
            return DatasetColumnSummary(self._column_summaries[columns])
        elif isinstance(columns, slice):
            columns = self._columns[columns]
        return DatasetColumnSummaryCollection(self._dataset, columns=columns)

    def __iter__(self) -> Iterable["DatasetColumnSummary"]:
        self._update()
        yield from [
            DatasetColumnSummary(self._column_summaries[c]) for c in self._columns
        ]

    def __repr__(self) -> str:
        string = "<"
        for c in self._columns[:-1]:
            string += "<" + c + " Summary>, "
        string += "<" + self._columns[-1] + " Summary>>"
        return string

    def __str__(self) -> str:
        string = ""
        for c in self._columns:
            string += str(DatasetColumnSummary(self._column_summaries[c])) + "\n"
        return string

    def _create_column_summary_dict(self, column: Any) -> Dict[str, Any]:
        summary = {}
        summary["name"] = column.name
        summary["data_type"] = column.data_type
        summary["logical_types"] = [
            k
            for k, v in self._dataset._logical_types.items()
            if v in column.logical_types
        ]
        summary["datetime_format"] = column.datetime_format
        if column.stats.is_numeric:
            stats = column.stats.numeric.dump()
        else:
            stats = column.stats.non_numeric.dump()
        summary["count"] = stats.get("count", 0)
        summary["missing"] = self._dataset.shape[0] - summary["count"]
        summary["mean"] = stats.get("mean", None)
        summary["std"] = stats.get("std", None)
        summary["min"] = stats.get("min", None)
        summary["max"] = stats.get("max", None)
        summary["unique"] = stats.get("unique")
        summary["freq"] = stats.get("freq")
        summary["hist"] = self._create_histogram_string(column)
        return summary

    def _create_histogram_string(self, column: Any) -> str:
        hist = ""
        if column.stats.is_numeric:
            ht = column.stats.numeric.hist_ticks
            hc = column.stats.numeric.hist_counts
            ht = [f"{ast.literal_eval(t):0.3g}" for t in ht]
            hc = [round(c / max(hc) * 20) for c in hc]
            max_len = max(len(ht[0]), len(ht[-1])) + 1
            hist += ht[0].rjust(max_len) + "|" + "\u2588" * hc[0] + "\n"
            for c in hc[1:-1]:
                hist += "|".rjust(max_len + 1) + "\u2588" * c + "\n"
            hist += ht[-1].rjust(max_len) + "|" + "\u2588" * hc[-1] + "\n"
        else:
            ht = column.stats.non_numeric.hist_ticks
            hc = column.stats.non_numeric.hist_counts
            hc = [round(c / max(hc) * 20) for c in hc]
            max_len = max([len(t) for t in ht]) + 1
            for i, c in enumerate(hc):
                hist += ht[i].rjust(max_len) + "|" + "\u2588" * c + "\n"
        return hist

    def _update(self) -> None:
        self._dataset._update()
        self._column_summaries = {
            c.name: self._create_column_summary_dict(c)
            for c in self._dataset._info.columns
            if c.name in self._columns
        }


class DatasetJob(_utils.ServerJob):
    """Monitor creation of a dataset on the Driverless AI server.

    Attributes:
        key: unique ID
    """

    def __init__(self, client: "_core.Client", key: str, name: str = None) -> None:
        super().__init__(client=client, key=key)
        self._name = name

    def _update(self) -> None:
        self._info = self._client._backend.get_dataset_job(self.key)

    def result(self, silent: bool = False) -> "Dataset":
        """Wait for job to complete, then return a Dataset object.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        if self._name:
            self._client._backend.update_dataset_name(self.key, self._name)
        return self._client.datasets.get(self._info.entity.key)


class Datasets:
    """Interact with datasets on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self._simple_connectors = {
            "azrbs": self._client._backend.create_dataset_from_azr_blob,
            "dtap": self._client._backend.create_dataset_from_dtap,
            "file": self._client._backend.create_dataset_from_file,
            "gbq": self._client._backend.create_dataset_from_gbq,
            "gcs": self._client._backend.create_dataset_from_gcs,
            "hdfs": self._client._backend.create_dataset_from_hadoop,
            "minio": self._client._backend.create_dataset_from_minio,
            "s3": self._client._backend.create_dataset_from_s3,
            "snow": self._client._backend.create_dataset_from_snowflake,
        }

    def _dataset_create(
        self,
        data: Union[str, "pandas.DataFrame"],
        data_source: str,
        data_source_config: Dict[str, str] = None,
        name: str = None,
    ) -> "DatasetJob":
        if data_source not in self._client.connectors.list():
            raise ValueError(
                "Please use one of the available connectors:",
                self._client.connectors.list(),
            )
        elif data_source in self._simple_connectors:
            key = self._simple_connectors[data_source](data)
        elif data_source == "upload":
            if data.__class__.__name__ == "DataFrame":
                with tempfile.NamedTemporaryFile(
                    prefix="Pandas_", suffix=".pkl"
                ) as pkl:
                    data.to_pickle(  # type: ignore
                        pkl.name, compression=None, protocol=4
                    )
                    key = self._client._backend.upload_dataset(pkl.name)[0]
            else:
                key = self._client._backend.upload_dataset(data)[0]
        elif data_source == "jdbc":
            if name is None:
                raise ValueError("JDBC connector requires a `name` argument.")
            spark_jdbc_config = self._client._server_module.protocol.SparkJDBCConfig(
                options=[],
                database=data_source_config.get("jdbc_default_config", ""),
                jarpath=data_source_config.get("jdbc_jar", ""),
                classpath=data_source_config.get("jdbc_driver", ""),
                url=data_source_config.get("jdbc_url", ""),
            )
            key = self._client._backend.create_dataset_from_spark_jdbc(
                dst=name,
                query=data,
                id_column=data_source_config.get("id_column", ""),
                jdbc_user=data_source_config["jdbc_username"],
                password=data_source_config["jdbc_password"],
                spark_jdbc_config=spark_jdbc_config,
            )
        elif data_source == "kdb":
            if name is None:
                raise ValueError("KDB connector requires a `name` argument.")
            key = self._client._backend.create_dataset_from_kdb(name, data)
        elif data_source == "recipe_file":
            data_file = self._client._backend.upload_custom_recipe_sync(
                data
            ).data_files[0]
            key = self._client._backend.create_dataset_from_recipe(data_file)
        elif data_source == "recipe_url":
            recipe_key = self._client._backend.create_custom_recipe_from_url(data)
            completed_recipe_job = _recipes.RecipeJob(self._client, recipe_key).result(
                silent=True
            )
            data_file = completed_recipe_job._info.entity.data_files[0]
            key = self._client._backend.create_dataset_from_recipe(data_file)
        return DatasetJob(self._client, key, name)

    def create(
        self,
        data: Union[str, "pandas.DataFrame"],
        data_source: str = "upload",
        data_source_config: Dict[str, str] = None,
        name: str = None,
    ) -> "Dataset":
        """Create a dataset on the Driverless AI server and return a Dataset
        object corresponding to the created dataset.

        Args:
            data: path to data or query for SQL based data sources
            data_source: name of connector to use for data transfer
                (use ``driverlessai.connectors.list()`` to see configured names)
            data_source_config: dictionary of configuration options for
                advanced connectors
            name: dataset name on the Driverless AI server
        """
        return self.create_async(data, data_source, data_source_config, name).result()

    def create_async(
        self,
        data: Union[str, "pandas.DataFrame"],
        data_source: str,
        data_source_config: Dict[str, str] = None,
        name: str = None,
    ) -> "DatasetJob":
        """Launch creation of a dataset on the Driverless AI server and return
        a DatasetJob object to track the status.

        Args:
            data: path to data or query for SQL based data sources
            data_source: name of connector to use for data transfer
                (use ``driverlessai.connectors.list()`` to see configured names)
            data_source_config: dictionary of configuration options for
                advanced connectors
            name: dataset name on the Driverless AI server
        """
        return self._dataset_create(data, data_source, data_source_config, name)

    def get(self, key: str) -> "Dataset":
        """Get a Dataset object corresponding to a dataset on the
        Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the dataset
        """
        info = self._client._backend.get_dataset_job(key).entity
        return Dataset(self._client, info)

    def gui(self) -> _utils.GUILink:
        """Get full URL for the user's datasets page on Driverless AI server."""
        return _utils.GUILink(f"{self._client.server.address}/#datasets")

    def list(self, start_index: int = 0, count: int = None) -> List["Dataset"]:
        """List of Dataset objects available to the user.

        Args:
            start_index: index on Driverless AI server of first dataset to list
            count: max number of datasets to request from the Driverless AI server
        """
        if count:
            return [
                self.get(d.key)
                for d in self._client._backend.list_datasets(
                    start_index, count, include_inactive=False
                ).datasets
            ]
        chunk_size = 100
        chunk_position = start_index
        datasets = []  # type: List["Dataset"]
        while True:
            chunk = self._client._backend.list_datasets(
                chunk_position, chunk_size, include_inactive=True
            ).datasets
            datasets.extend(
                self.get(d.key)
                for d in chunk
                if _utils.is_server_job_complete(d.import_status)
            )
            if len(chunk) < chunk_size:
                break
            chunk_position += chunk_size
        return datasets


class DatasetSplitJob(_utils.ServerJob):
    """Monitor splitting of a dataset on the Driverless AI server.

    Attributes:
        key: unique ID
    """

    def __init__(
        self,
        client: "_core.Client",
        key: str,
        train_name: str = None,
        test_name: str = None,
    ) -> None:
        super().__init__(client=client, key=key)
        self._test_name = test_name
        self._train_name = train_name

    def _update(self) -> None:
        self._info = self._client._backend.get_dataset_split_job(self.key)

    def result(self, silent: bool = False) -> Dict[str, "Dataset"]:
        """Wait for job to complete, then return a dictionary of Dataset objects.

        Args:
            silent: if True, don't display status updates
        """
        status_update = _utils.StatusUpdate()
        if not silent:
            status_update.display(_utils.JobStatus.RUNNING.message)
        self._wait(silent=True)
        ds1_key, ds2_key = self._info.entity
        ds1 = DatasetJob(self._client, ds1_key, name=self._train_name).result(
            silent=True
        )
        ds2 = DatasetJob(self._client, ds2_key, name=self._test_name).result(
            silent=True
        )
        if not silent:
            status_update.display(_utils.JobStatus.COMPLETE.message)
        status_update.end()
        return {"train_dataset": ds1, "test_dataset": ds2}

    def status(self, verbose: int = None) -> str:
        """Return short job status description string."""
        return self._status().message
