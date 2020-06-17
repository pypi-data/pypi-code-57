"""Base libary for RPA using TOS."""
import re
import warnings

from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from .deco import log_number_of_task_objects, handle_errors
from .exceptions import DataAlreadyProcessed
from .helpers import (
    handle_dead_selenium,
    handle_signals,
    take_screenshot,
)
from . import messages


class RPALibrary:
    """
    RPA Library base class to be used for writing Robot Framework
    libraries using TOSLibrary.

    This class contains error handling, logging, and TOS interaction,
    so users don't have to write them manually every time they write
    new keyword libraries.

    Every library inheriting RPALibrary must have a method
    ``main_action`` which defines the steps to be done for every
    task object in the current stage. To run the actions,
    call ``main_loop`` defined here (override only when necessary).

    Usage example:

    .. code-block:: python

        from TOSLibrary.RPALibrary import RPALibrary

        class PDFMerger(RPALibrary):

            def __init__(self):
                '''
                Remember to call ``super`` in the constructor.
                '''
                super(PDFMerger, self).__init__()
                self.merger = PdfFileMerger()

            @keyword
            def merge_all_pdfs(self, filename):
                '''
                Get every valid task object from the DB
                and do the action defined in ``main_action``.
                Exceptions are handled and logged appropriately.
                '''
                count = self.main_loop(current_stage=4)
                if count:
                    write_merged_pdf_object(filename)

            def main_action(self, to):
                '''Append pdf as bytes to the pdf merger object.'''
                pdf_bytes = io.BytesIO(to["payload"]["pdf_letter"])
                self.merger.append(pdf_bytes)

    And the corresponding Robot Framework script:

    .. code-block:: python

        *** Settings ***
        Library                 PDFMerger

        *** Tasks ***
        Manipulate PDF files
            Merge All PDFs      combined.pdf

    """

    def __init__(self, retry_limit_per_task_object=3, sort_condition=""):
        """Remember to call this constructor when inheriting.

        See the example in the :class:`~TOSLibrary.RPALibrary.RPALibrary`
        class docstring above.

        :ivar self.tags: Tags of the current Robot Framework task.
        :ivar self.tos: TOSLibrary instance of the current RF suite.
        :ivar self.error_msg: Library-wide general error message text.
        """
        super(RPALibrary, self).__init__()
        self.tags = BuiltIn().get_variable_value("@{TEST TAGS}")
        self.tos = BuiltIn().get_library_instance("TOSLibrary")
        self.error_msg = ""  # TODO: totally unused, deprecate this?
        self.processed_items = []
        self.consecutive_failures = 0
        self.retry_limit_per_task_object = retry_limit_per_task_object

        if sort_condition:
            warnings.warn("sort_condition should be passed to `main_loop` as kwarg", DeprecationWarning)
        self.sort_condition = sort_condition

    def _get_stage_from_tags(self):
        """Get the stage number from the stage tag.

        It is required that the current task tags include one tag
        of the form 'stage_0'.

        Example:

            >>> self.tags = ["stage_0", "producer"]
            >>> self._get_stage_from_tags()
            0
        """
        try:
            stage_tag = next(filter(lambda x: "stage" in x, self.tags))
            return int(re.search(r'\d+', stage_tag).group())
        except (StopIteration, ValueError):
            raise

    @keyword
    @log_number_of_task_objects
    def main_loop(self, *args, **kwargs):
        """
        The main loop for processing task objects on a given stage.

        Get task objects ready for processing and do the actions
        as defined in method ``main_action``. Continue doing this as
        long as valid task objects are returned from the DB. The counter
        value must be returned for logger decorator consumption.

        Using this method/keyword gives you automatic logging and looping
        over valid task objects. You can override this method to suit
        your specific needs.

        Remember to explicitly call this from Robot Framework.

        :param kwargs:

            - **stage** (`int` or `str`) - the current stage where this is called from.
              If this is not given, the stage is inferred from the Robot Framework
              task level tag.

            - **status** (`str`) - the status of the task objects to process
              (default is 'pass')

            - **change_status** (`bool`) - decide if the status should be changed after
              main_action or kept as the original (default is `True`).

            - **error_msg** (`str`) - Custom error message if the action here fails
              (optional).

            - **getter** (`callable`) - the method which is used to get the data to process.
              This might be a custom input data fetcher. By default it is
              ``find_one_task_object_by_status_and_stage``.
              Note that using a custom getter is still experimental.

            - **getter_args** (`dict`)- arguments that should be passed to the custom
              getter. By default they are ``{"statuses": status, "stages": previous_stage}``.

            - **amend** (`dict`) - additional MongoDB query to be used
              for filtering task objects (optional).

            - **main_keyword** (`str`) - custom method name to use in place of `main_action`
              (optional).

            - **sort_condition** (`str`) - custom condition to be used in sorting
              the task objects, e.g. `sort_condition=[("_id", pymongo.DESCENDING)]`
              (optional).


        :returns: number of task objects processed
        :rtype: int
        :ivar new_status: the new status returned from the ``handle_errors``
                          decorator.
        :type new_status: str
        """
        current_stage = kwargs.get("current_stage")
        if current_stage is None:
            current_stage = self._get_stage_from_tags()
        else:  # 0 is a valid case
            current_stage = int(current_stage)
        previous_stage = current_stage - 1
        self.error_msg = kwargs.get("error_msg", "")  # used inside the decorator
        if current_stage == 0:
            return self.main_loop_when_creating()

        status = kwargs.get("status", "pass")
        getter_args = (status, previous_stage)
        getter_args = {
            "statuses": status,
            "stages": previous_stage,
            "amend": kwargs.get("amend", ""),
            "sort_condition": kwargs.get("sort_condition", "") if not self.sort_condition else self.sort_condition,  # TODO: self.sort_condition is deprecated, will be removed
        }

        if kwargs.get("getter"):
            # TODO: Add tests
            getter = kwargs.get("getter")
            getter_args = kwargs.get("getter_args", getter_args)
        else:
            # this will change status to processing
            getter = self.tos.find_one_task_object_by_status_and_stage

        counter = 0
        while True:
            to = getter(**getter_args)
            if not to:
                break
            counter += 1

            logger.info(f"\n[ INFO ] Handling task object {to['_id']}", also_console=True)

            self._update_stage_object(to["_id"], current_stage)
            self._save_retry_metadata_if_retry(to, current_stage)
            value, new_status = self._error_handled_pre_and_main_action(to=to, *args, **kwargs)
            if kwargs.get("change_status", True):
                self._update_status(to["_id"], current_stage, new_status)
            else:
                # change back to the original status from 'processing'
                # FIXME: is this if block ever needed?
                self._update_status(to["_id"], current_stage, status)
            if new_status == "fail":
                to["last_error"] = value
                self._update_exceptions(to["_id"], current_stage, value)
                self._increment_fail_counter()
                if not kwargs.get("no_screenshots"):
                    take_screenshot()
                to = self._predefined_action_on_fail(to)
                self.action_on_fail(to)  # the process might be killed here
            else:
                self._reset_fail_counter()
            self.post_action(to, new_status)
            self.tos.set_stage_end_time(to["_id"], current_stage)

        return counter

    def _update_stage_object(self, object_id, current_stage):
        """Update stages object with new stage."""
        self.tos.set_task_object_stage(object_id, current_stage)
        self.tos.set_stage_start_time(object_id, current_stage)
        self.tos.set_stage_build_number(object_id, current_stage)
        self.tos.set_stage_executor(object_id, current_stage)

    def _update_status(self, object_id, current_stage, status):
        """Update stages object with new status."""
        self.tos.set_task_object_status(object_id, status)
        self.tos.set_stage_status(object_id, current_stage, status)

    def _update_exceptions(self, object_id, current_stage, value):
        """Update stages object with the new exception."""
        self.tos.set_task_object_last_error(object_id, value)
        self.tos.update_stage_exceptions(object_id, value, current_stage)

    def _save_retry_metadata_if_retry(self, to, current_stage):
        """
        For every run, check if it's a retry.
        If it is, populate a retry object inside the stage object.
        This way we get to know when and where the job has been running
        on failures.
        """
        # TODO: combine this with update_stage, they are mostly duplicate code
        if to.get("retry_count", 0) > 0:
            self._update_retries_data(
                to["_id"],
                current_stage,
                to["retry_count"]
            )

    def _update_retries_data(self, object_id, current_stage, retry_count):
        self.tos.set_retry_build_number(object_id, current_stage, retry_count)
        self.tos.set_retry_executor(object_id, current_stage, retry_count)

    @keyword
    @log_number_of_task_objects
    def main_loop_when_creating(self):
        """
        The main loop for creating new task objects.

        Call this as a Robot Framework keyword.

        When using this, define also a keyword method ``get_input_data``
        which must return ``None`` when no more data are available.
        """
        # TODO: this is useless at the moment
        counter = 0
        self._reset_processed_list()
        while True:
            data, status = self._error_handled_get_input_data()
            to = {}  # TODO: is it a good idea to use empty dict as default to?
            if status == "pass" and not data:
                # no more input data to process
                break
            elif status == "pass":
                self._check_if_input_data_already_processed(data)
                to = self.tos.create_new_task_object(data)
                self.tos.set_task_object_status(to["_id"], "pass")
            elif status == "fail":
                self.action_on_fail(to)
            self.post_action(to, status)
            counter += 1

        return counter

    @handle_errors()
    def _error_handled_pre_and_main_action(self, to=None, **kwargs):
        """Wrap the user defined main action with error handling.

        Firstly `pre_action` is called and so it is included in the
        error handling.

        It is important that the task object ``to`` is passed
        as a keyword argument to this method. It allows the decorator
        to consume the task object data.

        :param to: task object
        :type to: dict
        :param kwargs:
            - **main_keyword** (`str`) -  Name of the keyword that should be
              used as the ``main_action``

        :returns: return value of ``main_action`` and status ("pass" or "fail")
         as returned from the decorator ``handle_errors``.
        :rtype: `tuple`
        """
        handle_signals()
        handle_dead_selenium()
        to = self.pre_action(to)
        main_keyword = kwargs.get("main_keyword")
        if main_keyword:
            return BuiltIn().run_keyword(main_keyword, to)

        return self.main_action(to)

    @handle_errors()
    def _error_handled_get_input_data(self):
        return self.get_input_data()

    def get_input_data(self, *args):  # pragma: no cover
        """
        Get the raw data here.

        Should return ``None`` if no more input data is available.
        """
        # TODO: consider writing the functionality as a generator.
        pass

    def main_action(self, to):
        """
        The main action to do.

        You should make the implementation yourself.
        This will be called in the ``main_loop`` and should
        contain all the steps that should be done with the
        data stored in one task object.

        Don't call this from Robot Framework, call ``main_loop`` instead.

        :param to: task object
        :type to: dict
        """
        raise NotImplementedError("Make your own implementation of this method")

    def post_action(self, to, status, *args, **kwargs):
        """Teardown steps.

        Action to do for every task object after
        the main action has completed succesfully or failed.

        You should make the implementation yourself, if needed.

        :param to: task object
        :type to: dict
        :param status: status returned from running ``handle_errors`` decorated
                       ``main_action``.
        :type status: str
        """
        pass

    def pre_action(self, to):
        """Setup steps.

        Action to do for every task object before the error
        handled main action.

        You should make the implementation yourself, if needed.

        :param to: task object
        :type to: dict
        """
        return to

    def _predefined_action_on_fail(self, to):
        """Call error handler plugins here automatically."""
        logger.debug("Predefined action on fail not yet implemented")
        # TODO: call error handlers defined in errors.py with ErrorLibrary
        # (see branch WIP_error_handlers)
        # TODO: handle consecutive failure
        # TODO: handle too many retries
        # TODO: where should the retrying go?
        return to

    def action_on_fail(self, to):
        """Custom action to do when an error is encountered.

        This is always called after automatic error handlers
        have done their job. You can define here some custom
        action or some steps that should be always run after
        every error handler.

        E.g. fail the robot immediately with keyword "Fail".

        Note that these actions are not error handled, all exceptions
        will be propagated until Robot Framework stops execution with
        failure.
        """
        pass

    def _reset_processed_list(self):
        self.processed_items = []

    def _check_if_input_data_already_processed(self, data):
        """Failsafe preventing infinite loops."""
        # TODO: is this a good idea at all?
        data_hash = hash(frozenset(data.items()))
        if data_hash in self.processed_items:
            raise DataAlreadyProcessed("Input data was just processed")
        else:
            self.processed_items.append(data_hash)

    def _increment_fail_counter(self):
        self.consecutive_failures += 1

    def _reset_fail_counter(self):
        """Call this when the whole workflow has completed succesfully
        for one task object.

        This resets the consecutive failure counter.
        """
        self.consecutive_failures = 0
