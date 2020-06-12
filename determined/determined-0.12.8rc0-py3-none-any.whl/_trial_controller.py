import abc
import logging
import pathlib
from typing import Any, Dict, List, Optional, cast

import determined as det
from determined import constants, horovod, ipc, workload
from determined._rendezvous_info import RendezvousInfo
from determined.horovod import hvd
from determined_common import check
from determined_common.types import StepID


class TrialController(metaclass=abc.ABCMeta):
    """
    Abstract base class for TrialControllers.

    A TrialController is the lowest Determined-owned layer of the harness. It consumes Workloads
    from higher layers of the harness and applies framework-specific logic to execute the
    workloads.  Framework-specific details like tf.Session objects or keras.Model objects are
    handled at this level.

    Because framework APIs vary significantly, there is a wide variation in how TrialControllers
    are implemented. There are presently two major subclasses of TrialControllers:
    CallbackTrialController and LoopTrialController.

    CallbackTrialController is the legacy form of TrialController. It requires
    framework logic to be reentrant and controlled via function calls. It is
    currently only used in the integration test framework.

    LoopTrialController is the newer form of TrialController. It are distinguished by being
    designed to require owning the main control loop in the code, which is a prerequisite for
    using horovod for distributed training.
    """

    def __init__(
        self,
        context: Any,
        env: det.EnvContext,
        workloads: workload.Stream,
        load_path: Optional[pathlib.Path],
        rendezvous_info: RendezvousInfo,
        hvd_config: horovod.HorovodContext,
    ) -> None:
        self.context = context
        self.env = env
        self.workloads = workloads
        self.load_path = load_path
        self.rendezvous_info = rendezvous_info
        self.hvd_config = hvd_config

        self._check_if_trial_supports_configurations(env)

    @staticmethod
    @abc.abstractmethod
    def pre_execute_hook(env: det.EnvContext, hvd_config: horovod.HorovodContext) -> Any:
        """
        Certain things must be initialized before either running user code (in the Native API case)
        or intializing user code (in the Trial API case).
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def from_trial(
        trial_inst: "det.Trial",
        context: det.TrialContext,
        env: det.EnvContext,
        workloads: workload.Stream,
        load_path: Optional[pathlib.Path],
        rendezvous_info: RendezvousInfo,
        hvd_config: horovod.HorovodContext,
    ) -> "TrialController":
        """
        Create a TrialController from an instantiated framework-matched Trial.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def from_native(
        context: det.NativeContext,
        env: det.EnvContext,
        workloads: workload.Stream,
        load_path: Optional[pathlib.Path],
        rendezvous_info: RendezvousInfo,
        hvd_config: horovod.HorovodContext,
    ) -> "TrialController":
        """
        Create a TrialController from either a generic Experiment object or a framework-matched
        Experiment object.
        """
        pass

    @abc.abstractmethod
    def run(self) -> None:
        """
        The main control loop for executing user code.
        """
        pass

    @staticmethod
    def supports_multi_gpu_training() -> bool:
        return False

    @staticmethod
    def supports_mixed_precision() -> bool:
        return False

    @staticmethod
    def supports_averaging_training_metrics() -> bool:
        return False

    def initialize_wrapper(self) -> None:
        pass

    @staticmethod
    def support_determined_native() -> bool:
        return False

    def _check_if_trial_supports_configurations(self, env: det.EnvContext) -> None:
        if self.env.experiment_config.slots_per_trial() > 1:
            check.true(
                self.supports_multi_gpu_training(),
                "Multi-gpu training is not supported for this "
                "framework interface. Please set slots_per_task = 1.",
            )

        if self.env.experiment_config.mixed_precision_enabled():
            check.true(
                self.supports_mixed_precision(),
                "Mixed precision training is not supported for this framework interface. "
                'Please set `mixed_precision = "O0"`.',
            )

        if env.experiment_config.native_enabled():
            check.true(self.support_determined_native())

        if env.experiment_config.averaging_training_metrics_enabled():
            check.true(self.supports_averaging_training_metrics())


class CallbackTrialController(TrialController):
    """
    Abstract base class for the legacy, callback-based TrialControllers.

    Frameworks should create framework-specific subclasses and implement :func:`train_for_step`,
    :func:`compute_validation_metrics`, :func:`save`, and :func:`load`.
    """

    @staticmethod
    def from_native(*args: Any, **kwargs: Any) -> "TrialController":
        raise NotImplementedError("CallbackTrialControllers do not support the Native API")

    def run(self) -> None:
        """
        A basic control loop of the old-style (callback-based) TrialController
        classes.
        """

        for w, args, response_func in self.workloads:
            try:
                if w.kind == workload.Workload.Kind.RUN_STEP:
                    check.len_eq(args, 1)
                    check.is_instance(args[0], int)
                    num_batches = cast(int, args[0])
                    response = self.train_for_step(
                        w.step_id, num_batches
                    )  # type: workload.Response
                elif w.kind == workload.Workload.Kind.COMPUTE_VALIDATION_METRICS:
                    response = self.compute_validation_metrics(w.step_id)
                elif w.kind == workload.Workload.Kind.CHECKPOINT_MODEL:
                    check.len_eq(args, 1)
                    check.is_instance(args[0], pathlib.Path)
                    path = cast(pathlib.Path, args[0])
                    self.save(path)
                    response = {}
                elif w.kind == workload.Workload.Kind.TERMINATE:
                    self.terminate()
                    response = workload.Skipped()
                else:
                    raise AssertionError("Unexpected workload: {}".format(w.kind))

            except det.errors.SkipWorkloadException:
                response = workload.Skipped()

            response_func(response)

    # Methods implemented by AF-specific subclasses.
    @abc.abstractmethod
    def train_for_step(self, step_id: StepID, batches_per_step: int) -> Dict[str, Any]:
        """
        Runs a trial for one step, which should consist of the training
        the model on the given number of batches.  Implemented by frameworks.

        Args:
            step_id: The index of the step to run.  This controls which batches
                to run.
            batches_per_step: How many batches per step to run.
            batch_loader: The training batch loader instance. Depending on the
                framework implementation, a batch loader may or may not be
                needed.

        Returns:
            The training metrics computed for each batch in the step.
        """
        pass

    @abc.abstractmethod
    def compute_validation_metrics(self, step_id: StepID) -> Dict[str, Any]:
        """
        Computes validation metrics for a trial given the current
        trial state.  Implemented by frameworks.

        Args:
            step_id: The index of the step to run.

            batch_loader: The validation batch loader instance. Depending on
                the framework implementation, a batch loader may or may not be
                needed.

        Returns:
            The validation metrics.
        """
        pass

    @abc.abstractmethod
    def save(self, path: pathlib.Path) -> None:
        """
        Saves the current model state to persistent storage. Implemented by
        frameworks.

        Args:
            path: A directory on the container file system; the trial
                should create the directory and checkpoint its current
                state into one or more files inside that directory. The
                implementation of this function creates `path`; hence,
                it should not exist before this function is called.
        """
        pass

    @abc.abstractmethod
    def load(self, path: pathlib.Path) -> None:
        """
        Loads the current model state from persistent storage. Implemented
        by frameworks.

        Args:
            path: A directory on the container file system.
        """
        pass

    def terminate(self) -> None:
        pass


class LoopTrialController(TrialController):
    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)  # type: ignore

        self.batch_size = self.context.get_per_slot_batch_size()
        self.batches_per_step = self.env.experiment_config.batches_per_step()

        logging.debug("Starting LoopTrialController initialization.")

        if self.hvd_config.use:
            self.is_chief = hvd.rank() == 0
            training_process_rank = hvd.local_rank()
        else:
            self.is_chief = self.rendezvous_info.get_rank() == 0
            training_process_rank = 0

        if self.hvd_config.use and not self.is_chief:
            log_level = (
                logging.DEBUG if self.env.experiment_config.debug_enabled() else logging.WARNING
            )
            logging.getLogger().setLevel(log_level)

        logging.debug(
            f"Training coordination initialized on local rank {training_process_rank}, "
            f"using hvd: {self.hvd_config.use}."
        )

        # Initialize communication directly between training processes.
        self.train_process_comm_chief = None  # type: Optional[ipc.ZMQServer]
        self.train_process_comm_worker = None  # type: Optional[ipc.ZMQClient]
        if self.hvd_config.use:
            self._initialize_train_process_comm()

    def _initialize_train_process_comm(self) -> None:
        check.true(self.hvd_config.use)
        if self.is_chief:
            logging.debug(
                f"Chief {hvd.rank()} setting up server with "
                f"port {constants.INTER_TRAIN_PROCESS_COMM_PORT}."
            )
            self.train_process_comm_chief = ipc.ZMQServer(
                ports=[constants.INTER_TRAIN_PROCESS_COMM_PORT], num_connections=1
            )
        else:
            chief_ip_address = self.rendezvous_info.get_ip_addresses()[0]
            logging.debug(
                f"Non-Chief {hvd.rank()} setting up comm to "
                f"{chief_ip_address} w/ port {constants.INTER_TRAIN_PROCESS_COMM_PORT}."
            )
            self.train_process_comm_worker = ipc.ZMQClient(
                ip_address=chief_ip_address, port=constants.INTER_TRAIN_PROCESS_COMM_PORT
            )
