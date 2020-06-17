# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Callbacks rules classes and helpers
"""
import logging

from ._vendors.sqreen_security_signal_sdk import Signal
from ._vendors.wrapt import FunctionWrapper
from .condition_evaluator import ConditionEvaluator, is_condition_empty
from .constants import LIFECYCLE_METHODS
from .remote_exception import raw_traceback_formatter, traceback_formatter
from .runtime_infos import get_agent_type
from .runtime_storage import runtime
from .utils import HAS_TYPING, now

if HAS_TYPING:
    from datetime import datetime
    from typing import Optional

LOGGER = logging.getLogger(__name__)


class BaseCallback(object):
    """ Base class for callbacks.

    The hook_name is the path to the hook, it could be either a module, like
    "package.module", or a specific class "package.module::Class".
    The hook_name is the name of the function to hook_on, it's relative to
    the hook_module, for example with a hook_module equal to
    "package.module::Class" and a hook_path equal to "method", we will
    hook on the method named "method" of a class named "Class" in the module
    named "package.module"
    """

    SUPPORTS_BUDGET = False  # override constants in subclasses supporting it
    INTERRUPTIBLE = True

    def __init__(self, hook_module, hook_name, strategy=None):
        self.hook_module = hook_module
        self.hook_name = hook_name
        self.strategy = strategy

    @property
    def collaborative(self):
        """Is the callback collaborative and support running with a budget."""
        return self.SUPPORTS_BUDGET

    @property
    def skippable(self):
        """Allow the callback to be skipped if request is overtime."""
        return self.INTERRUPTIBLE


def check_condition_wrapper(rule_data, function, condition, lifecycle):
    """ Wrapper that will check lifecycle method pre-condition before
    calling it.
    If pre-conditions are true, call the lifecycle method, otherwise
    return None.
    """

    def wrapper(wrapped, callback, _args, _kwargs):
        """ Wrapper around lifecycle method
        """

        def extract_args(instance, args, kwargs, result=None, exc_info=None,
                         **options):
            return (instance, args, kwargs, result, exc_info)

        inst, args, kwargs, result, exc_info = extract_args(*_args, **_kwargs)

        # Get the storage from the callback if available
        storage = callback.storage if callback is not None else runtime

        # Compute return value depending on the lifecycle method we wrap
        rv = result if lifecycle == "post" else exc_info

        binding_eval_args = {
            "request": storage.get_current_request(),
            "response": storage.get_current_response(),
            "inst": inst,
            "args": storage.get_current_args(args),
            "kwargs": kwargs,
            "data": rule_data,
            "rv": rv,
        }

        # Check the pre condition
        condition_result = condition.evaluate(**binding_eval_args)

        LOGGER.debug(
            "ConditionWrapper (%s) result for %s: %s",
            condition,
            function,
            condition_result,
        )

        if condition_result in (False, None):
            return None

        # Execute the hook otherwise with the original args
        return wrapped(*_args, **_kwargs)

    return FunctionWrapper(function, wrapper)


def call_count_wrapper(function, lifecycle, observation_key):
    """ Wrapper around lifecycle methods that record number of calls
    """

    def wrapper(wrapped, callback, args, kwargs):
        """ Record the number of calls for this callback lifecycle method.
        Buffer the number in the callback itself (self.call_counts) and record
        an observation every X times, X being the field call_count_interval of
        the rule.
        """
        current_count = callback.call_counts[lifecycle]

        if current_count + 1 == callback.call_count_interval:
            callback.record_observation(
                "sqreen_call_counts", observation_key, callback.call_count_interval
            )
            callback.call_counts[lifecycle] = 0
        else:
            callback.call_counts[lifecycle] += 1

        return wrapped(*args, **kwargs)

    return FunctionWrapper(function, wrapper)


def perf_monitoring_wrapper(function, name):
    """ Wrapper that will monitor the performance of the rule callback.
    It will time the execution of the callback and send it as an
    observation metric.

    The wrapper should be called first before every others.
    """

    def wrapper(wrapped, callback, args, kwargs):
        """ Time the callback execution.
        """
        # Get the storage from the callback if available
        storage = callback.storage if callback is not None else runtime

        with storage.trace(name):
            return wrapped(*args, **kwargs)

    return FunctionWrapper(function, wrapper)


class RuleCallback(BaseCallback):

    SECTIONS = ("request", "response", "params", "headers", "context")

    def __init__(
        self,
        hook_module,
        hook_name,
        rule_name,
        rulespack_id,
        runner,
        beta=False,
        block=False,
        test=False,
        strategy_cls=None,
        data=None,
        conditions=None,
        callbacks=None,
        call_count_interval=0,
        metrics=None,
        payload_sections=None,
        priority=None,
        attack_render_info=None,
        attack_type=None,
        storage=runtime,
    ):
        super(RuleCallback, self).__init__(
            hook_module, hook_name, strategy_cls
        )
        self.rule_name = rule_name
        self.rulespack_id = rulespack_id

        if data is None:
            data = {}
        self.data = data
        self.beta = beta
        self.block = block
        self.test = test
        self.runner = runner
        self.metrics = metrics
        self.storage = storage

        if conditions is None:
            conditions = {}
        self.conditions = conditions

        if callbacks is None:
            callbacks = {}
        self.callbacks = callbacks
        self.attack_render_info = attack_render_info
        self.attack_type = attack_type

        # Callbacks
        self.call_count_interval = call_count_interval
        self.call_counts = {"pre": 0, "post": 0, "failing": 0}

        self._apply_conditions()
        self._apply_call_count()
        self._apply_perf_monitoring()

        # Payload sections.
        if payload_sections is None:
            payload_sections = self.SECTIONS
        self.payload_sections = payload_sections

        # Priority (lower number means higher priority)
        self.priority = priority if priority is not None else 100

    @classmethod
    def from_rule_dict(cls, rule_dict, runner, storage=runtime):
        """ Return a RuleCallback based on a rule dict
        """
        return cls(
            hook_module=rule_dict["hookpoint"]["klass"],
            hook_name=rule_dict["hookpoint"]["method"],
            rule_name=rule_dict["name"],
            rulespack_id=rule_dict["rulespack_id"],
            strategy_cls=rule_dict["hookpoint"].get("strategy", "import_hook"),
            attack_render_info=rule_dict["hookpoint"].get("attack_render_info", {}),
            beta=rule_dict.get("beta", False),
            block=rule_dict.get("block", False),
            test=rule_dict.get("test", False),
            data=rule_dict.get("data"),
            conditions=rule_dict.get("conditions"),
            callbacks=rule_dict.get("callbacks"),
            call_count_interval=rule_dict.get("call_count_interval", 0),
            runner=runner,
            metrics=rule_dict.get("metrics", []),
            payload_sections=rule_dict.get("payload"),
            priority=rule_dict.get("priority"),
            attack_type=rule_dict.get("attack_type"),
            storage=storage,
        )

    @property
    def performance_monitoring_enabled(self):
        """ Return True if the performance monitoring is enabled for this rule.
        """
        if self.runner is not None:
            return self.runner.performance_metrics and self.runner.performance_metrics_settings.enabled()
        return False

    def get_remaining_budget(self, callback_kwargs=None):
        """ Get the remaining time we have for running this callback according
        to the request budget if there is one. The budget can be overriden
        with a special option in kwargs. Return None otherwise.
        """
        if callback_kwargs is not None:
            override_budget = callback_kwargs.pop("__sqreen_override_budget", None)
            if override_budget is not None:
                return override_budget
        if self.runner is not None and self.performance_monitoring_enabled:
            budget = self.runner.budget
            if budget is not None:
                return budget - (self.storage.request_sq_time or 0)

    def _apply_conditions(self):
        """ Wrap each lifecycle methods if the Rule define them and if we have
        conditions for them.
        """
        for lifecycle in LIFECYCLE_METHODS.values():
            conditions = self.conditions.get(lifecycle)

            if not is_condition_empty(conditions) and hasattr(self, lifecycle):
                conditions = ConditionEvaluator(conditions)

                # Wrap the lifecycle method
                lifecycle_method = getattr(self, lifecycle)
                wrapped = check_condition_wrapper(
                    self.data, lifecycle_method, conditions, lifecycle)
                setattr(self, lifecycle, wrapped)

    def _apply_call_count(self):
        # Only count calls if call_count_interval is > 0
        if self.call_count_interval == 0:
            return

        for lifecycle in LIFECYCLE_METHODS.values():
            if hasattr(self, lifecycle):
                lifecycle_method = getattr(self, lifecycle)

                observation_key = "%s/%s/%s" % (
                    self.rulespack_id,
                    self.rule_name,
                    lifecycle,
                )

                wrapped = call_count_wrapper(
                    lifecycle_method, lifecycle, observation_key)
                setattr(self, lifecycle, wrapped)

    def _apply_perf_monitoring(self):
        # Only enable the performance monitoring if the feature flag is
        if not self.performance_monitoring_enabled:
            return

        for lifecycle in LIFECYCLE_METHODS.values():
            if hasattr(self, lifecycle):
                lifecycle_method = getattr(self, lifecycle)

                metric_name = "sq.{}.{}".format(self.rule_name, lifecycle)

                # Register the performance metric if it does not exist yet
                if self.runner is not None \
                        and not self.runner.metrics_store.is_registered(metric_name):
                    self.runner.metrics_store.register_metric(
                        metric_name, "Binning",
                        self.runner.performance_metrics_settings.period,
                        base=self.runner.performance_metrics_settings.base,
                        unit=self.runner.performance_metrics_settings.unit
                    )

                wrapped = perf_monitoring_wrapper(
                    lifecycle_method, metric_name)
                setattr(self, lifecycle, wrapped)

    def exception_infos(self, infos={}):
        """ Returns additional infos in case of exception
        """
        return {"rule_name": self.rule_name, "rulespack_id": self.rulespack_id}

    def record_attack(self, infos=None, at=None):
        """Record an attack."""
        if at is None:
            at = now()
        payload = {
            "infos": infos,
            "rulespack_id": self.rulespack_id,
            "rule_name": self.rule_name,
            "beta": self.beta,
            "block": self.block,
            "test": self.test,
            "attack_type": self.attack_type,
            "time": at,
        }
        if "context" in self.payload_sections:
            current_request = self.storage.get_current_request()
            if current_request:
                payload["backtrace"] = list(current_request.raw_caller)
        LOGGER.debug("Observed attack %r", payload)
        self.storage.observe("attacks", payload, self.payload_sections)

    def record_observation(self, metric_name, key, value, at=None):
        """Record a metric observation."""

        self.global_record_observation(metric_name, key, value, at, storage=self.storage)

    @classmethod
    def global_record_observation(cls, metric_name, key, value, at=None, storage=runtime):
        """Record a metric observation"""

        if at is None:
            at = now()
        payload = (metric_name, at, key, value)
        LOGGER.debug("Observed metric %r", payload)
        storage.observe("observations", payload, report=False)

    def record_exception(self, exc, exc_info, stack=None, infos=None, at=None):
        """Record an exception."""
        if infos is None:
            infos = {}
        if at is None:
            at = now()
        # Try to recover some infos from the exception if it's a
        # SqreenException.
        try:
            infos.update(exc.exception_infos())
        except Exception:
            pass
        bt = raw_traceback_formatter(exc_info[2])
        if stack is not None:
            bt = traceback_formatter(stack) + bt
        payload = {
            "message": str(exc_info[1]),
            "klass": exc_info[0].__name__,
            "infos": infos,
            "rule_name": self.rule_name,
            "rulespack_id": self.rulespack_id,
            "test": self.test,
            "time": at,
            "backtrace": bt,
        }
        LOGGER.debug("Observed exception %r", payload)
        self.storage.observe("sqreen_exceptions", payload, self.payload_sections)

    def record_overtime(self, lifecycle=None, at=None):
        """Record an overtime execution."""
        if at is None:
            at = now()
        name = self.rule_name
        if lifecycle is not None:
            name += ".{}".format(lifecycle)
        payload = ("request_overbudget_cb", at, name, 1)
        LOGGER.debug("Observed overbudget callback %r", payload)
        self.storage.observe("overtime_callbacks", payload, report=False)

    def record_trace(self, scope, payload, at=None):
        # type: (str, dict, Optional[datetime]) -> bool
        """Record a tracing signal."""
        if at is None:
            at = now()
        sampler = self.runner.tracing_sampler
        if sampler is None:
            return False
        decision = sampler.should_sample(scope=scope, at=at)
        if not decision:
            return False
        signal = Signal(
            type="point",  # type: ignore
            signal_name="tracing.{}".format(scope),
            payload_schema="tracing/{}-2020-04-21".format(scope),
            payload=payload,
            source="sqreen:agent:{}".format(get_agent_type()),
            trigger=decision.attrs["trigger"],
            time=at,
        )
        if self.storage.get_current_request():
            LOGGER.debug("Observed signal %r", signal)
            self.storage.observe("signals", signal)
            return True
        elif self.runner.signal_client is not None:
            LOGGER.debug("Sending signal %r", signal)
            self.runner.signal_client.signal(**signal)
            return True
        return False

    @property
    def lifecycle_methods(self):
        return [
            lifecycle
            for lifecycle in LIFECYCLE_METHODS.values()
            if hasattr(self, lifecycle)
        ]

    @property
    def whitelisted(self):
        """ Return True if the callback should be skipped (whitelisted
        request), False otherwise
        """
        return self.storage.get_whitelist_match() or False

    def __repr__(self):
        return "%s(rule_name=%r)" % (self.__class__.__name__, self.rule_name)
