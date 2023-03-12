import inspect
import logging
from functools import wraps
from typing import Any

from opentelemetry import trace

from app.core.config import settings
from app.helpers.jaeger import trace_handler

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

def trace_func(span_name=None, ignore_first_args=False, max_length=4096):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if not settings.JAEGER_ENABLED and settings.JAEGER_MODE:
                return function(*args, **kwargs)

            span_name_ = span_name if span_name else function.__name__
            tracer_args = args[:]
            if len(tracer_args) >= 1 and ignore_first_args:
                tracer_args = tracer_args[1:]

            with tracer.start_as_current_span(name=span_name_) as span:
                result = function(*args, **kwargs)
                trace_handler(span, span_name_, *tracer_args, max_length=max_length, **kwargs)
                return result
        return wrapper
    return decorator


def inject_jaeger_to_obj(obj: Any, max_length=4096):
    for k, v in inspect.getmembers(obj):
        if k[0] == '_':
            continue
        if callable(v):
            span_name = f"{type(obj).__name__}.{k}"
            new_v = trace_func(span_name=span_name, max_length=max_length)(v)
            if inspect.ismethod(v):
                setattr(obj, k, new_v)


def inject_jaeger_to_class(max_length=4096):
    def decorate(cls):
        for k, v in cls.__dict__.items():
            if k[0] == '_':
                continue
            if callable(v):
                span_name = f"{cls.__name__}.{k}"
                setattr(cls, k, trace_func(span_name=span_name, max_length=max_length)(v))
        return cls
    return decorate
