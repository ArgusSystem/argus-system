from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

prop = TraceContextTextMapPropagator()
TRACE_PARENT_KEY = 'traceparent'


def get_tracer(host, port, service_name='argus'):
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: service_name})
        )
    )

    tracer = trace.get_tracer(__name__)

    jaeger_exporter = JaegerExporter(
        agent_host_name=host,
        agent_port=port,
    )

    span_processor = BatchSpanProcessor(jaeger_exporter)

    trace.get_tracer_provider().add_span_processor(span_processor)

    return tracer


def set_span_in_context(span):
    return trace.set_span_in_context(span)


def get_trace_parent(context=None):
    carrier = {}
    prop.inject(carrier, context)
    return carrier[TRACE_PARENT_KEY]


def get_context(trace_parent):
    return prop.extract({TRACE_PARENT_KEY: trace_parent})
