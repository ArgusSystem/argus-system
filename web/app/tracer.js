const { BatchSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const {
  defaultTextMapGetter,
  ROOT_CONTEXT,
} = require('@opentelemetry/api');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { W3CTraceContextPropagator } = require('@opentelemetry/core');

const configuration = require('./configuration');

const serviceName = 'argus-web-server';

const exporter = new JaegerExporter({
  tags: [],
  endpoint: configuration['tracing']['endpoint']
});

const provider = new NodeTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: serviceName
  })
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();

const propagator = new W3CTraceContextPropagator();

function extract(traceParent) {
  return propagator.extract(ROOT_CONTEXT, {'traceparent': traceParent}, defaultTextMapGetter)
}

module.exports = {
  tracer: provider.getTracer(serviceName),
  get_context: extract
};