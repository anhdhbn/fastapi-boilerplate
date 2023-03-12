from typing import Any

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.proto.grpc import \
    JaegerExporter as GrpcJaegerExporter
from opentelemetry.exporter.jaeger.thrift import \
    JaegerExporter as ThriftJaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from opentelemetry.trace import Span
from pydantic import BaseModel
from sqlalchemy import Engine

from app.core.config import settings
from app.helpers.enums import JaegerModeEnum


def setup_jaeger_app(app: FastAPI):
    trace.set_tracer_provider(TracerProvider(
            sampler=TraceIdRatioBased(rate=settings.JAEGER_SAMPLING_RATE),
            resource=Resource.create({
                SERVICE_NAME: settings.PROJECT_NAME
            })
        ))

    if settings.JAEGER_MODE == JaegerModeEnum.ThriftAgent:
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(ThriftJaegerExporter(
                agent_host_name=settings.JAEGER_HOST,
                agent_port=settings.JAEGER_PORT,
                udp_split_oversized_batches=True,
            ))
        )
    elif settings.JAEGER_MODE == JaegerModeEnum.ThriftCollector:
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(ThriftJaegerExporter(
                collector_endpoint=settings.JAEGER_COLLECTOR_ENDPOINT,
                udp_split_oversized_batches=True,
            ))
        )
    elif settings.JAEGER_MODE == JaegerModeEnum.Grpc:
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(GrpcJaegerExporter(
                collector_endpoint=settings.JAEGER_COLLECTOR_ENDPOINT,
                insecure=settings.JAEGER_INSECURE,
            ))
        )
    
    FastAPIInstrumentor().instrument_app(app=app, excluded_urls=settings.JAEGER_EXCLUDED_URLS)

def setup_jaeger_sqlalchemy(engine: Engine):
    SQLAlchemyInstrumentor().instrument(
        engine=engine,
    )

def preprocess_attrs(obj: Any, max_length=4096) -> str:
    result = str(obj)
    if isinstance(obj, BaseModel):
        result = str(obj.dict())
    return result[:int(max_length)]

def trace_handler(span: Span, span_name: str, *args, max_length=4096, result=None, **kwargs):
    ignore_keys = ['max_length', 'span_name']
    attrs = {
        f'{span_name}.args': [arg for arg in args],
    }

    for k, v in kwargs.items():
        attrs.update({
            f'{span_name}.kwargs.{k}': v,
        })
    attrs.update({
        f'{span_name}.result': result,
    })

    final_attrs = {}
    for k, v in attrs.items():
        if v is None:
            continue
        if k in ignore_keys:
            continue
        final_attrs.update({
            k: preprocess_attrs(v, max_length=max_length)
        })
    span.set_attributes(final_attrs)
