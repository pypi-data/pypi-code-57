"""Experiments module of official Python client for Driverless AI."""

import csv
import functools
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple, Union

from driverlessai import _core
from driverlessai import _datasets
from driverlessai import _recipes
from driverlessai import _utils


class Experiment(_utils.ServerJob):
    """Interact with an experiment on the Driverless AI server.

    Attributes:
     artifacts (ExperimentArtifacts): interact with artifacts that are created
         when the experiment completes
     key (str): unique ID
     log (ExperimentLog): interact with experiment logs
     train_dataset (Dataset): training dataset for the experiment
     validation_dataset (Dataset): validation dataset for the experiment
     test_dataset (Dataset): test dataset for the experiment
     settings (Dict[str, Any]): experiment settings
    """

    def __init__(self, client: "_core.Client", key: "str") -> None:
        super().__init__(client=client, key=key)
        self.name = ""
        self._update()
        self.artifacts = ExperimentArtifacts(self)
        self.log = ExperimentLog(self)
        # Datasets
        train_dataset = client.datasets.get(self._info.entity.parameters.dataset.key)
        validation_dataset = None
        test_dataset = None
        if self._info.entity.parameters.validset.key != "":
            validation_dataset = client.datasets.get(
                self._info.entity.parameters.validset.key
            )
        if self._info.entity.parameters.testset.key != "":
            test_dataset = client.datasets.get(self._info.entity.parameters.testset.key)
        self.datasets = {
            "train_dataset": train_dataset,
            "validation_dataset": validation_dataset,
            "test_dataset": test_dataset,
        }
        # Settings
        self.settings = self._client.experiments._parse_server_settings(
            self._info.entity.parameters.dump()
        )

    def __repr__(self) -> str:
        return f"{self.__class__} {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    def _format_notification(self, notification: str) -> str:
        return notification.replace("\n", "\n\n")

    def _get_retrain_settings(
        self,
        use_smart_checkpoint: bool = False,
        final_pipeline_only: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        # Get parent experiment settings
        settings = {**self.datasets, **self.settings}  # type: Dict[str, Any]
        # Remove settings that shouldn't be reused
        settings.pop("name", None)
        # Update settings with any new settings
        settings.update(kwargs)
        # Set parent experiment
        settings["parent_experiment"] = self
        if use_smart_checkpoint:
            settings["feature_brain_level"] = 1003
        if final_pipeline_only:
            settings["feature_brain_level"] = 1003
            settings["time"] = 0
        return settings

    def _model_ready(func: Callable) -> Callable:  # type: ignore
        @functools.wraps(func)
        def check(self: "Experiment", *args: Any, **kwargs: Any) -> Callable:
            if self.is_complete():
                return func(self, *args, **kwargs)
            raise RuntimeError("Experiment is not complete: " + self.status(verbose=2))

        return check

    def _update(self) -> None:
        self._info = self._client._backend.get_model_job(self.key)
        self.name = self._info.entity.description

    def abort(self) -> None:
        """Terminate experiment immediately and only generate logs."""
        if self.is_running():
            return self._client._backend.abort_experiment(self.key)

    def delete(self) -> None:
        """Permanently delete experiment from the Driverless AI server."""
        self._client._backend.delete_model(self.key)
        time.sleep(1)  # hack for https://github.com/h2oai/h2oai/issues/14519
        print("Driverless AI Server reported experiment", self, "deleted.")

    def finish(self) -> None:
        """Finish experiment by jumping to final pipeline training and generating
        experiment artifacts.
        """
        if self.is_running():
            return self._client._backend.stop_experiment(self.key)

    def gui(self) -> _utils.GUILink:
        """Get full URL for the experiment's page on the Driverless AI server."""
        return _utils.GUILink(
            f"{self._client.server.address}/#experiment?key={self.key}"
        )

    def metrics(self) -> Dict[str, Union[str, float]]:
        """Return dictionary of experiment scorer metrics and AUC metrics,
        if available.
        """
        self._update()
        metrics = {}
        metrics["scorer"] = self._info.entity.score_f_name

        metrics["val_score"] = self._info.entity.valid_score
        metrics["val_score_sd"] = self._info.entity.valid_score_sd
        metrics["val_roc_auc"] = self._info.entity.valid_roc.auc
        metrics["val_pr_auc"] = self._info.entity.valid_roc.aucpr

        metrics["test_score"] = self._info.entity.test_score
        metrics["test_score_sd"] = self._info.entity.test_score_sd
        metrics["test_roc_auc"] = self._info.entity.test_roc.auc
        metrics["test_pr_auc"] = self._info.entity.test_roc.aucpr

        return metrics

    def notifications(self) -> List[str]:
        """Return list of experiment notifications."""
        self._update()
        return [self._format_notification(n) for n in self._info.entity.warnings]

    @_model_ready
    def predict(
        self,
        dataset: "_datasets.Dataset",
        include_columns: List[str] = None,
        include_raw_outputs: bool = False,
        include_shap_values: bool = False,
    ) -> "Prediction":
        """Predict on a dataset, then return a Prediction object.

        Args:
            dataset: a Dataset object corresonding to a dataset on the
                Driverless AI server
            include_columns: list of columns from the dataset to append to the
                prediction csv
            include_raw_outputs: append predictions as margins (in link space) to the
                prediction csv
            include_shap_values: append feature contributions to the prediction csv
        """
        return self.predict_async(
            dataset, include_columns, include_raw_outputs, include_shap_values
        ).result()

    @_model_ready
    def predict_async(
        self,
        dataset: "_datasets.Dataset",
        include_columns: List[str] = None,
        include_raw_outputs: bool = False,
        include_shap_values: bool = False,
    ) -> "PredictionJobs":
        """Launch prediction job on a dataset and return a PredictionJobs object
        to track the status.

        Args:
            dataset: a Dataset object corresonding to a dataset on the
                Driverless AI server
            include_columns: list of columns from the dataset to append to the
                prediction csv
            include_raw_outputs: append predictions as margins (in link space) to the
                prediction csv
            include_shap_values: append feature contributions to the prediction csv
        """
        if include_columns is None:
            include_columns = []
        # note that `make_prediction` has 3 mutually exclusive options that
        # create different csvs, which is why it has to be called up to 3 times
        keys = []
        # creates csv of probabilities
        keys.append(
            self._client._backend.make_prediction(
                self.key,
                dataset.key,
                output_margin=False,
                pred_contribs=False,
                keep_non_missing_actuals=False,
                include_columns=include_columns,
            )
        )
        if include_raw_outputs:
            # creates csv of raw outputs only
            keys.append(
                self._client._backend.make_prediction(
                    self.key,
                    dataset.key,
                    output_margin=True,
                    pred_contribs=False,
                    keep_non_missing_actuals=False,
                    include_columns=[],
                )
            )
        if include_shap_values:
            # creates csv of SHAP values only
            keys.append(
                self._client._backend.make_prediction(
                    self.key,
                    dataset.key,
                    output_margin=False,
                    pred_contribs=True,
                    keep_non_missing_actuals=False,
                    include_columns=[],
                )
            )
        jobs = [PredictionJob(self._client, key, dataset.key, self.key) for key in keys]

        # The user will get a single csv created by concatenating all the above csvs.
        # From the user perspective they are creating a single csv even though
        # multiple csv jobs are spawned. The PredictionJobs object allows the
        # multiple jobs to be interacted with as if they were a single job.
        return PredictionJobs(
            self._client,
            jobs,
            dataset.key,
            self.key,
            include_columns,
            include_raw_outputs,
            include_shap_values,
        )

    def rename(self, name: str) -> "Experiment":
        """Change experiment display name.

        Args:
            name: new display name
        """
        self._client._backend.update_model_description(self.key, name)
        self._update()
        return self

    def result(self, silent: bool = False) -> "Experiment":
        """Wait for training to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def retrain(
        self,
        use_smart_checkpoint: bool = False,
        final_pipeline_only: bool = False,
        **kwargs: Any,
    ) -> "Experiment":
        """Create a new model using the same datasets and settings. Through
        ``kwargs`` it's possible to pass new datasets or overwrite settings.

        Args:
            use_smart_checkpoint: start training from last smart checkpoint
            final_pipeline_only: trains a final pipeline using smart checkpoint
                if available, otherwise uses default hyperparameters
            kwargs: datasets and experiment settings as defined in
                ``experiments.create()``
        """
        return self.retrain_async(
            use_smart_checkpoint, final_pipeline_only, **kwargs
        ).result()

    def retrain_async(
        self,
        use_smart_checkpoint: bool = False,
        final_pipeline_only: bool = False,
        **kwargs: Any,
    ) -> "Experiment":
        """Launch creation of a new experiment using the same datasets and
        settings. Through `kwargs` it's possible to pass new datasets or
        overwrite settings.

        Args:
            use_smart_checkpoint: start training from last smart checkpoint
            final_pipeline_only: trains a final pipeline using smart checkpoint
                if available, otherwise uses default hyperparameters
            kwargs: datasets and experiment settings as defined in
                ``experiments.create()``
        """
        settings = self._get_retrain_settings(
            use_smart_checkpoint, final_pipeline_only, **kwargs
        )
        return self._client.experiments.create_async(**settings)

    def summary(self) -> None:
        """Print experiment summary."""
        if not _utils.is_server_job_complete(self._status()):
            print("Experiment is not complete:", self.status(verbose=2))
            return
        print(self._info.message)
        variable_importance = self._client._backend.get_variable_importance(
            self.key
        ).dump()
        print("Variable Importance:")
        for v in range(len(variable_importance["gain"])):
            gain = f"{variable_importance['gain'][v]:.2f}"
            interaction = variable_importance["interaction"][v]
            description = variable_importance["description"][v].split(" [internal:")[0]
            print(" ", gain, "|", interaction, "|", description)

    def variable_importance(self) -> Union[_utils.Table, None]:
        """Get variable importance in a Table."""
        try:
            variable_importance = self._client._backend.get_variable_importance(
                self.key
            ).dump()
            return _utils.Table(
                [list(x) for x in zip(*variable_importance.values())],
                variable_importance.keys(),
            )
        except self._client._server_module.protocol.RemoteError:
            print("Variable importance not available.")
            return None


class ExperimentArtifacts:
    def __init__(self, experiment: "Experiment") -> None:
        self._experiment = experiment
        self._paths = {}  # type: Dict[str, str]

    def _get_path(self, attr: str, do_timeout: bool = True, timeout: int = 60) -> str:
        path = getattr(self._experiment._info.entity, attr)
        if not do_timeout:
            return path
        seconds = 0
        while path == "" and seconds < timeout:
            time.sleep(1)
            seconds += 1
            self._experiment._update()
            path = getattr(self._experiment._info.entity, attr)
        return path

    def _model_ready(func: Callable) -> Callable:  # type: ignore
        @functools.wraps(func)
        def check(self: "ExperimentArtifacts", *args: Any, **kwargs: Any) -> Callable:
            if self._experiment.is_complete():
                return func(self, *args, **kwargs)
            raise RuntimeError(
                "Experiment is not complete: " + self._experiment.status(verbose=2)
            )

        return check

    def _update(self) -> None:
        self._experiment._update()
        self._paths["autoreport"] = self._get_path(
            "autoreport_path", self._experiment.settings.get("make_autoreport", False)
        )
        self._paths["logs"] = self._get_path("log_file_path")
        self._paths["mojo_pipeline"] = self._get_path(
            "mojo_pipeline_path",
            self._experiment.settings.get("make_mojo_pipeline", "off") == "on",
        )
        self._paths["python_pipeline"] = self._get_path(
            "scoring_pipeline_path",
            self._experiment.settings.get("make_python_scoring_pipeline", "off")
            == "on",
        )
        self._paths["summary"] = self._get_path("summary_path")
        self._paths["test_predictions"] = self._get_path("test_predictions_path", False)
        self._paths["train_predictions"] = self._get_path(
            "train_predictions_path", False
        )
        self._paths["val_predictions"] = self._get_path("valid_predictions_path", False)

    @_model_ready
    def create(self, artifact: str) -> None:
        """(Re)build certain artifacts, if possible.

        (re)buildable artifacts:

        - ``'autoreport'``
        - ``'mojo_pipeline'``
        - ``'python_pipeline'``

        Args:
            artifact: name of artifact to (re)build
        """
        if artifact == "python_pipeline":
            print("Building Python scoring pipeline...")
            if not self._experiment._client._backend.build_scoring_pipeline_sync(
                self._experiment.key
            ).file_path:
                print("Unable to build Python scoring pipeline.")
        if artifact == "mojo_pipeline":
            print("Building MOJO pipeline...")
            if not self._experiment._client._backend.build_mojo_pipeline_sync(
                self._experiment.key
            ).file_path:
                print("Unable to build MOJO pipeline.")
        if artifact == "autoreport":
            print("Generating autoreport...")
            if not self._experiment._client._backend.make_autoreport_sync(
                self._experiment.key, template="", config=""
            ).report_path:
                print("Unable to generate autoreport.")

    @_model_ready
    def download(
        self,
        only: Union[str, List[str]] = None,
        dst_dir: str = ".",
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Download experiment artifacts from the Driverless AI server. Returns
        a dictionary of relative paths for the downloaded artifacts.

        Args:
            only: specify specific artifacts to download
            dst_dir: relative path to directory where the experiment artifacts
                should be saved
            overwrite: overwrite existing files
        """
        self._update()
        dst_paths = {}
        if isinstance(only, str):
            only = [only]
        if only is None:
            only = self.list()
        for k in only:
            path = self._paths[k]
            if path:
                dst_paths[k] = self._experiment._client._download(
                    path, dst_dir, overwrite
                )
            else:
                print("'", k, "' does not exist on the Driverless AI server.", sep="")
        return dst_paths

    @_model_ready
    def list(self) -> List[str]:
        """List of experiment artifacts that exist on the Driverless AI server."""
        self._update()
        return [k for k, v in self._paths.items() if v]


class ExperimentLog:
    """Interact with experiment logs."""

    def __init__(self, experiment: "Experiment") -> None:
        self._client = experiment._client
        self._experiment = experiment
        self._log_name = "h2oai_experiment_" + experiment.key + ".log"

    def _error_message(self) -> str:
        self._experiment._update()
        error_message = (
            "No logs available for experiment " + self._experiment.name + "."
        )
        return error_message

    def download(
        self, dst_dir: str = ".", archive: bool = True, overwrite: bool = False
    ) -> str:
        """Download experiment logs from the Driverless AI server.

        Args:
            dst_dir: relative path to directory where logs should be saved
            archive: if available, prefer downloding an archive that contains
                multiple log files and stack traces if any were created
            overwrite: overwrite existing file
        """
        self._experiment._update()
        log_name = self._experiment._info.entity.log_file_path
        if log_name == "" or not archive:
            log_name = self._log_name
        return self._client._download(log_name, dst_dir, overwrite)

    def head(self, num_lines: int = 50) -> None:
        """Print first n lines of experiment log.

        Args:
            num_lines: number of lines to print
        """
        with tempfile.TemporaryDirectory() as log_dir:
            try:
                log_file = self._client._download(
                    self._log_name, log_dir, overwrite=True, verbose=False
                )
                with open(log_file, encoding="utf-8") as log:
                    for line in log.readlines()[:num_lines]:
                        print(line.strip())
            except self._client._server_module.protocol.RequestError:
                print(self._error_message())
            except Exception as e:
                print(e)

    def tail(self, num_lines: int = 50) -> None:
        """Print last n lines of experiment log.

        Args:
            num_lines: number of lines to print
        """
        with tempfile.TemporaryDirectory() as log_dir:
            try:
                log_file = self._client._download(
                    self._log_name, log_dir, overwrite=True, verbose=False
                )
                with open(log_file, encoding="utf-8") as log:
                    for line in log.readlines()[-num_lines:]:
                        print(line.strip())
            except self._client._server_module.protocol.RequestError:
                print(self._error_message())
            except Exception as e:
                print(e)


class Experiments:
    """Interact with experiments on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self._default_experiment_settings = {
            setting.name.strip(): self._sanitize_server_setting(setting.val)
            for setting in client._backend.get_all_config_options()
        }
        if self._client._backend.get_gpu_stats().gpus == 0:
            self._default_experiment_settings["num_gpus_per_experiment"] = 0
            self._default_experiment_settings["num_gpus_per_model"] = 0
        # convert setting name from key to value
        self._setting_for_server_dict = {
            "drop_columns": "cols_to_drop",
            "fold_column": "fold_col",
            "scorer": "score_f_name",
            "target_column": "target_col",
            "time_column": "time_col",
            "weight_column": "weight_col",
        }
        self._setting_for_api_dict = {
            v: k for k, v in self._setting_for_server_dict.items()
        }

    def _parse_api_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Python API experiment settings to format required by the
        Driverless AI server.
        """
        custom_settings = {}

        tasks = ["classification", "regression"]

        not_config_overrides = [
            "train_dataset",  # 'dataset',
            "resumed_model",
            "target_column",  # 'target_col',
            "weight_column",  # 'weight_col',
            "fold_column",  # 'fold_col',
            "orig_time_col",
            "time_column",  # 'time_col',
            "is_classification",
            "drop_columns",  # 'cols_to_drop',
            "validset",
            "testset",
            "enable_gpus",
            "seed",
            "accuracy",
            "time",
            "interpretability",
            "scorer",  # 'score_f_name',
            "time_groups_columns",
            "time_period_in_seconds",
            "num_prediction_periods",
            "num_gap_periods",
            "is_timeseries",
            # 'config_overrides',
            "custom_feature",
        ]

        for setting in [
            "config_overrides",
            "validation_dataset",
            "test_dataset",
            "parent_experiment",
        ]:
            if setting not in settings or settings[setting] is None:
                settings[setting] = ""

        def get_ref(desc: str, obj: Any) -> Tuple[str, Any]:
            if isinstance(obj, str):
                key = obj
            else:
                key = obj.key
            if desc == "train_dataset":
                ref_type = "dataset"
                ref = self._client._server_module.references.DatasetReference(key)
            if desc == "validation_dataset":
                ref_type = "validset"
                ref = self._client._server_module.references.DatasetReference(key)
            if desc == "test_dataset":
                ref_type = "testset"
                ref = self._client._server_module.references.DatasetReference(key)
            if desc == "parent_experiment":
                ref_type = "resumed_model"
                ref = self._client._server_module.references.ModelReference(key)
            return ref_type, ref

        included_models = []
        for m in settings.pop("models", []):
            if isinstance(m, _recipes.ModelRecipe):
                included_models.append(m.name)
            else:
                included_models.append(m)
        if len(included_models) > 0:
            settings.setdefault("included_models", [])
            settings["included_models"] += included_models

        included_transformers = []
        for t in settings.pop("transformers", []):
            if isinstance(t, _recipes.TransformerRecipe):
                included_transformers.append(t.name)
            else:
                included_transformers.append(t)
        if len(included_transformers) > 0:
            settings.setdefault("included_transformers", [])
            settings["included_transformers"] += included_transformers

        custom_settings["is_timeseries"] = False
        custom_settings["enable_gpus"] = self._client._backend.get_gpu_stats().gpus > 0
        custom_settings["config_overrides"] = settings["config_overrides"]
        for setting, value in settings.items():
            if setting == "task":
                if value not in tasks:
                    raise ValueError("Please set the task to one of:", tasks)
                custom_settings["is_classification"] = "classification" == value
            elif setting in [
                "train_dataset",
                "validation_dataset",
                "test_dataset",
                "parent_experiment",
            ]:
                ref_type, ref = get_ref(setting, value)
                custom_settings[ref_type] = ref
            elif setting == "time_column":
                custom_settings[self._setting_for_server_dict[setting]] = value
                custom_settings["is_timeseries"] = value is not None
            elif setting == "scorer":
                if isinstance(value, _recipes.ScorerRecipe):
                    value = value.name
                custom_settings[self._setting_for_server_dict[setting]] = value
            elif setting == "enable_gpus":
                if custom_settings[setting]:  # confirm GPUs are present
                    custom_settings[setting] = value
            elif setting in self._setting_for_server_dict:
                custom_settings[self._setting_for_server_dict[setting]] = value
            elif setting in not_config_overrides:
                custom_settings[setting] = value
            elif setting != "config_overrides":
                if setting not in self._default_experiment_settings:
                    raise RuntimeError(
                        f"'{setting}' experiment setting not recognized."
                    )
                value = str(value)
                value = value.translate(value.maketrans("", "", "[]'"))
                if value.lower() in ["true", "false"]:
                    value = value.lower()
                elif not _utils.is_number(value):
                    value = "'" + value + "'"
                custom_settings["config_overrides"] += "\n" + setting + "=" + value

        server_settings = self._client._backend.get_experiment_tuning_suggestion(
            dataset_key=settings["train_dataset"].key,
            target_col=custom_settings["target_col"],
            is_classification=custom_settings["is_classification"],
            is_time_series=custom_settings["is_timeseries"],
            config_overrides=custom_settings["config_overrides"],
            cols_to_drop=custom_settings.get("cols_to_drop", []),
        ).dump()

        server_settings.update(**custom_settings)

        return server_settings

    def _parse_server_settings(self, server_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Driverless AI server experiment settings to Python API format."""
        blacklist = [
            "is_classification",
            "is_timeseries",
            "dataset",
            "validset",
            "testset",
            "orig_time_col",
            "resumed_model",
            "enable_gpus",
            "config_overrides",
        ]

        def task(server_settings: Dict[str, Any]) -> str:
            if server_settings["is_classification"]:
                return "classification"
            else:
                return "regression"

        settings = {"task": task(server_settings)}  # type: Dict[str, Any]
        if server_settings["seed"] is False:
            blacklist.append("seed")
        if server_settings["is_timeseries"] is False:
            blacklist.append("time_col")
        for key, value in server_settings.items():
            if key not in blacklist and value not in [None, "", []]:
                settings[self._setting_for_api_dict.get(key, key)] = value
        config_overrides = server_settings["config_overrides"].split("\n")
        for setting in config_overrides:
            setting = setting.split("=")
            setting_name = setting[0].strip()
            if setting_name in self._default_experiment_settings:
                default_value = self._default_experiment_settings[setting_name]
                current_value = self._sanitize_server_setting(setting[1])
                current_value_as_list = None
                if isinstance(current_value, str):
                    current_value_as_list = [
                        _utils.try_eval(x) for x in current_value.split(",") if x != ""
                    ]
                if (
                    current_value != default_value
                    and current_value_as_list != default_value
                ):
                    settings[setting_name] = current_value
        if (
            server_settings["resumed_model"]["key"] != ""
            and server_settings["resumed_model"]["display_name"] != ""
        ):
            settings["parent_experiment"] = self.get(
                server_settings["resumed_model"]["key"]
            )

        for setting_names in [
            ("included_models", "models"),
            ("included_transformers", "transformers"),
        ]:
            if setting_names[0] in settings and isinstance(
                settings[setting_names[0]], str
            ):
                settings[setting_names[1]] = settings.pop(setting_names[0]).split(",")

        return settings

    def _sanitize_server_setting(self, value: str) -> Any:
        sanitized_value = str(value)  # type: Any
        sanitized_value = sanitized_value.strip()
        sanitized_value = sanitized_value.replace('"', "'")
        sanitized_value = sanitized_value.strip("'")
        if sanitized_value.startswith("[") or _utils.is_number(value):
            sanitized_value = _utils.try_eval(sanitized_value)
        if sanitized_value in ["True", "true"]:
            sanitized_value = True
        if sanitized_value in ["False", "false"]:
            sanitized_value = False
        return sanitized_value

    def create(
        self,
        train_dataset: "_datasets.Dataset",
        target_column: str,
        task: str,
        name: str = None,
        **kwargs: Any,
    ) -> "Experiment":
        """Launch an experiment on the Driverless AI server and wait for it to
        complete before returning.

        Args:
            train_dataset: Dataset object
            target_column: name of column in ``train_dataset``
            task: one of ``'regression'`` or ``'classification'``
            name: display name for experiment
            kwargs:
            - accuracy (int): accuracy setting [1-10]
            - time (int): time setting [1-10]
            - interpretability (int): interpretability setting [1-10]
            - scorer (Union[str,ScorerRecipe]): metric to optimize for
            - models (Union[str,ModelRecipe]): limit experiment to these models
            - transformers (Union[str,TransformerRecipe]): limit experiment to
              these transformers
            - validation_dataset (Dataset): Dataset object
            - test_dataset (Dataset): Dataset object
            - weight_column (str): name of column in ``train_dataset``
            - fold_column (str): name of column in ``train_dataset``
            - time_column (str): name of column in ``train_dataset``,
              containing time ordering for timeseries problems
            - time_groups_columns (List[str]): list of column names,
              contributing to time ordering
            - drop_columns (List[str]): list of column names to be dropped
            - seed (int): seed for PRNG
            - time_period_in_seconds (int): the length of the time period in seconds,
              used in timeseries problems
            - num_prediction_periods (int): timeseries forecast horizont in time
              period units
            - num_gap_periods (int): number of time periods after which forecast starts

        .. note:: to see expert settings, use ``experiments.search_expert_settings()``.
        """
        return self.create_async(
            train_dataset, target_column, task, name, **kwargs
        ).result()

    def create_async(
        self,
        train_dataset: "_datasets.Dataset",
        target_column: str,
        task: str,
        name: str = None,
        **kwargs: Any,
    ) -> "Experiment":
        """Launch an experiment on the Driverless AI server and return an
        Experiment object to track the experiment status.

        Args:
            train_dataset: Dataset object
            target_column: name of column in ``train_dataset``
            task: one of ``'regression'`` or ``'classification'``
            name: display name for experiment
            kwargs:
            - accuracy (int): accuracy setting [1-10]
            - time (int): time setting [1-10]
            - interpretability (int): interpretability setting [1-10]
            - scorer (Union[str,ScorerRecipe]): metric to optimize for
            - models (Union[str,ModelRecipe]): limit experiment to these models
            - transformers (Union[str,TransformerRecipe]): limit experiment to
              these transformers
            - validation_dataset (Dataset): Dataset object
            - test_dataset (Dataset): Dataset object
            - weight_column (str): name of column in ``train_dataset``
            - fold_column (str): name of column in ``train_dataset``
            - time_column (str): name of column in ``train_dataset``,
              containing time ordering for timeseries problems
            - time_groups_columns (List[str]): list of column names,
              contributing to time ordering
            - drop_columns (List[str]): list of column names to be dropped
            - seed (int): seed for PRNG
            - time_period_in_seconds (int): the length of the time period in seconds,
              used in timeseries problems
            - num_prediction_periods (int): timeseries forecast horizont in time
              period units
            - num_gap_periods (int): number of time periods after which forecast starts

        .. note:: to see expert settings, use ``experiments.search_expert_settings()``.
        """
        if target_column not in train_dataset.columns:
            raise ValueError(
                f"Target column '{target_column}' not found in training data."
            )
        kwargs["task"] = task
        kwargs["train_dataset"] = train_dataset
        kwargs["target_column"] = target_column
        server_settings = self._parse_api_settings(kwargs)
        job_key = self._client._backend.start_experiment(
            self._client._server_module.messages.ModelParameters(**server_settings),
            experiment_name=name,
        )
        job = self.get(job_key)
        print("Experiment launched at:", job.gui())
        return job

    def get(self, key: str) -> "Experiment":
        """Get an Experiment object corresponding to an experiment on the
        Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the experiment
        """
        return Experiment(self._client, key)

    def gui(self) -> _utils.GUILink:
        """Get full URL for the experiments page on the Driverless AI server."""
        return _utils.GUILink(f"{self._client.server.address}/#experiments")

    def list(self, start_index: int = 0, count: int = None) -> List["Experiment"]:
        """List of Experiment objects available to the user.

        Args:
            start_index: index on Driverless AI server of first experiment in list
            count: number of experiments to request from the Driverless AI server
        """
        if count:
            return [
                self.get(m.key)
                for m in self._client._backend.list_models(start_index, count).models
            ]
        chunk_size = 100
        chunk_position = start_index
        experiments = []  # type: List["Experiment"]
        while True:
            chunk = [
                self.get(m.key)
                for m in self._client._backend.list_models(
                    chunk_position, chunk_size
                ).models
            ]
            experiments += chunk
            if len(chunk) < chunk_size:
                break
            chunk_position += chunk_size
        return experiments

    def preview(
        self,
        train_dataset: "_datasets.Dataset",
        target_column: str,
        task: str,
        **kwargs: Any,
    ) -> None:
        """Print a preview of experiment for the given settings.

        Args:
            train_dataset: Dataset object
            target_column: name of column in ``train_dataset``
            task: one of ``'regression'`` or ``'classification'``
            name: display name for experiment
            kwargs:
            - accuracy (int): accuracy setting [1-10]
            - time (int): time setting [1-10]
            - interpretability (int): interpretability setting [1-10]
            - scorer (Union[str,ScorerRecipe]): metric to optimize for
            - models (Union[str,ModelRecipe]): limit experiment to these models
            - transformers (Union[str,TransformerRecipe]): limit experiment to
              these transformers
            - validation_dataset (Dataset): Dataset object
            - test_dataset (Dataset): Dataset object
            - weight_column (str): name of column in ``train_dataset``
            - fold_column (str): name of column in ``train_dataset``
            - time_column (str): name of column in ``train_dataset``,
              containing time ordering for timeseries problems
            - time_groups_columns (List[str]): list of column names,
              contributing to time ordering
            - drop_columns (List[str]): list of column names to be dropped
            - seed (int): seed for PRNG
            - time_period_in_seconds (int): the length of the time period in seconds,
              used in timeseries problems
            - num_prediction_periods (int): timeseries forecast horizont in time
              period units
            - num_gap_periods (int): number of time periods after which forecast starts

        .. note:: to see expert settings, use ``experiments.search_expert_settings()``.
        """
        if target_column not in train_dataset.columns:
            raise ValueError(
                f"Target column '{target_column}' not found in training data."
            )
        kwargs["task"] = task
        kwargs["train_dataset"] = train_dataset
        kwargs["target_column"] = target_column
        settings = self._parse_api_settings(kwargs)
        preview = self._client._backend.get_experiment_preview_sync(
            dataset_key=settings["dataset"].key,
            validset_key=settings["validset"].key,
            classification=settings["is_classification"],
            dropped_cols=settings["cols_to_drop"],
            target_col=settings["target_col"],
            is_time_series=settings["is_timeseries"],
            time_col=settings["time_col"],
            enable_gpus=settings["enable_gpus"],
            accuracy=settings["accuracy"],
            time=settings["time"],
            interpretability=settings["interpretability"],
            reproducible=settings["seed"],
            resumed_experiment_id=settings["resumed_model"].key,
            config_overrides=settings["config_overrides"],
        )
        for line in preview:
            print(line)

    def search_expert_settings(
        self, search_term: str, show_description: bool = False
    ) -> None:
        """Search expert settings and print results. Useful when looking for
        kwargs to use when creating experiments.

        Args:
            search_term: term to search for (case insensitive)
            show_description: include description in results
        """
        for c in self._client._backend.get_all_config_options():
            if (
                search_term.lower()
                in " ".join([c.name, c.category, c.description, c.comment]).lower()
            ):
                print(
                    self._setting_for_api_dict.get(c.name, c.name),
                    "|",
                    "default_value:",
                    self._default_experiment_settings[c.name.strip()],
                    end="",
                )
                if show_description:
                    description = c.description.strip()
                    comment = " ".join(
                        [s.strip() for s in c.comment.split("\n")]
                    ).strip()
                    print(" |", description)
                    print(" ", comment)
                print()


class Prediction:
    """Interact with predictions from the Driverless AI server.

    Attributes:
        included_dataset_columns (List[str]): columns from dataset that are
            appended to predictions
        includes_raw_outputs (bool): whether predictions as margins (in link space)
            were appended to predictions
        includes_shap_values (bool): whether feature contributions were
            appended to predictions
        keys (Dict[str,str]):
            dataset: unique ID of dataset used to make predictions
            experiment: unique ID of experiment used to make predictions
            prediction: unique ID of predictions
    """

    def __init__(
        self,
        prediction_jobs: List["PredictionJob"],
        included_dataset_columns: List[str],
        includes_raw_outputs: bool,
        includes_shap_values: bool,
    ) -> None:
        self._client = prediction_jobs[0]._client
        self._jobs = prediction_jobs
        self.included_dataset_columns = included_dataset_columns
        self.includes_raw_outputs = includes_raw_outputs
        self.includes_shap_values = includes_shap_values
        self.keys = prediction_jobs[0].keys

    def download(self, dst_dir: str = ".", overwrite: bool = False) -> str:
        """Download csv of predictions.

        Args:
            dst_dir: relative path to directory where csv should be saved
            overwrite: overwrite existing file
        """
        if len(self._jobs) == 1:
            return self._client._download(
                self._jobs[0]._info.entity.predictions_csv_path, dst_dir, overwrite
            )

        with tempfile.TemporaryDirectory() as pred_dir:
            tmp_paths = [
                self._client._download(
                    job._info.entity.predictions_csv_path,
                    pred_dir,
                    overwrite=True,
                    verbose=False,
                )
                for job in self._jobs
            ]
            dst_path = Path(dst_dir, Path(tmp_paths[0]).name)
            # concatenate csvs horizontally
            with open(dst_path, "w", encoding="utf-8") as f:
                csv_writer = csv.writer(f)
                # read in multiple csvs
                csvs = [csv.reader(open(p, encoding="utf-8")) for p in tmp_paths]
                # unpack and join
                for row_from_each_csv in zip(*csvs):
                    row_joined = sum(row_from_each_csv, [])  # type: List[str]
                    csv_writer.writerow(row_joined)
            print(f"Downloaded '{dst_path}'")
            return str(dst_path)


class PredictionJob(_utils.ServerJob):
    """Monitor creation of predictions on the Driverless AI server.

    Attributes:
        keys (Dict[str,str]):
            dataset: unique ID of dataset used to make predictions
            experiment: unique ID of experiment used to make predictions
            prediction: unique ID of predictions
    """

    def __init__(
        self, client: "_core.Client", key: str, dataset_key: str, experiment_key: str
    ) -> None:
        super().__init__(client=client, key=key)
        self.keys = {
            "dataset": dataset_key,
            "experiment": experiment_key,
            "prediction": key,
        }

    def _update(self) -> None:
        self._info = self._client._backend.get_prediction_job(self.key)

    def result(self, silent: bool = False) -> "PredictionJob":
        """Wait for job to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def status(self, verbose: int = None) -> str:
        """Return short job status description string."""
        return self._status().message


class PredictionJobs(_utils.ServerJobs):
    """Monitor creation of predictions on the Driverless AI server.

    Attributes:
        included_dataset_columns (List[str]): columns from dataset that are
            appended to predictions
        includes_raw_outputs (bool): whether predictions as margins (in link space)
            are appended to predictions
        includes_shap_values (bool): whether feature contributions are
            appended to predictions
        keys (Dict[str,str]):
            dataset: unique ID of dataset used to make predictions
            experiment: unique ID of experiment used to make predictions
            prediction: unique ID of predictions
    """

    def __init__(
        self,
        client: "_core.Client",
        jobs: List[PredictionJob],
        dataset_key: str,
        experiment_key: str,
        include_columns: List[str],
        include_raw_outputs: bool,
        include_shap_values: bool,
    ) -> None:
        super().__init__(client=client, jobs=jobs)
        self.included_dataset_columns = include_columns
        self.includes_raw_outputs = include_raw_outputs
        self.includes_shap_values = include_shap_values
        self.keys = {
            "dataset": dataset_key,
            "experiment": experiment_key,
            "prediction": jobs[0].key,
        }

    def result(self, silent: bool = False) -> Any:
        """Wait for all jobs to complete.

        Args:
            silent: if True, don't display status updates
        """
        status_update = _utils.StatusUpdate()
        if not silent:
            status_update.display(_utils.JobStatus.RUNNING.message)
        jobs = [job.result(silent=True) for job in self.jobs]
        if not silent:
            status_update.display(_utils.JobStatus.COMPLETE.message)
        status_update.end()
        return Prediction(
            jobs,
            self.included_dataset_columns,
            self.includes_raw_outputs,
            self.includes_shap_values,
        )
