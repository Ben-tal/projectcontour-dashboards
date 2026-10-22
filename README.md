# [Contour Ingress Metrics Dashboard](https://grafana.com/grafana/dashboards/21396-contour-ingress-metrics/)

## Overview
The [contour-ingress-metrics](./contour-ingress-metrics.json) Grafana dashboard comprehensively monitors the Project Contour Ingress Controller at the service level, offering a detailed view of various service-level statistics. The dashboard is designed to help you understand the performance, availability, and overall health of your ingress resources.

## Dashboard Sections

### 1. Overview
- **Requests (period)**: Estimated request count during the selected dashboard time range (`increase`).
- **Connections (period)**: Estimated number of newly established upstream TCP connections during the selected dashboard time range (`increase`), not current active connections.
- **% Success (period)**: Percentage of successful requests over the period.
- **Requests (5m)**: Estimated request count during the preceding five minutes.
- **Connections (5m)**: Estimated number of newly established TCP connections during the preceding five minutes.
- **% Success (5m)**: Success rate of requests in the last 5 minutes.
- **HTTP Status Codes (5m)**: Estimated response counts by HTTP status class during the preceding five minutes.

### 2. Request Information
- **Ingress Success Requests (non 4|5xx Responses)**: Rate of successful ingress requests.
- **Ingress Failed Requests (4|5xx Responses)**: Rate of failed ingress requests.
- **Ingress Success Rate (non-4|5xx Responses)**: Success rate of ingress requests excluding 4xx and 5xx responses.

### 3. Service Summary
- **Ingress**: Overall ingress metrics.
- **Requests Per Second**: Rate of incoming requests per second.
- **Connections Per Second**: Rate of new upstream TCP connection establishments per second (`rate`); active connections are a separate gauge.
- **Latency (P50, P90, P99)**: Latency metrics at 50th, 90th, and 99th percentiles.

### 4. Throughput
- **Upstream Network Traffic**: Network traffic to upstream services.

### 5. Requests
- **Total Active Requests**: Current request concurrency (an active gauge).
- **New Requests (2m)**: Estimated new request count during the preceding two minutes at each point (`increase`), not a per-second rate.
- **Ingress Requests per Second**: New upstream requests per second (`rate`).

### 6. Connections
- **Total Active Connections**: Current connection concurrency (an active gauge).
- **New Connections (2m)**: Estimated new TCP connection count during the preceding two minutes at each point (`increase`), not a per-second rate.
- **Ingress Connections per Second**: New upstream TCP connections per second (`rate`). Envoy can reuse pooled connections, so this can be zero while requests continue.

# [Contour Global Metrics](https://grafana.com/grafana/dashboards/21402-contour-global-metrics/)
A Dashboard that monitors general statistics for Contour Ingress Controller (Projectcontour)

## Overview
The [contour-global-metrics](./contour-global-metrics.json) monitors general and more global statistics for Contour Ingress Controller. It displays real-time metrics for requests, connections, memory usage, and node status to help maintain and optimize performance.

## Features
- Requests Per Second (RPS): per-second throughput from the request counter.
- Active Requests: current request concurrency from an active gauge.
- Connections Per Second (CPS): new TCP connection establishments per second.
- Active Connections: current connection concurrency from an active gauge.
- Memory Usage
- Node Status
- HTTPProxy Resource Status

## Counts, rates, and active gauges

A counter `increase` estimates the number of events during a window: **period** uses the selected dashboard time range, **5m** uses the preceding five minutes, and **2m** uses the preceding two minutes at each chart point. `rate` reports events per second. Active gauges report current concurrent requests or connections. Prometheus extrapolates counter changes to window boundaries, so estimated counts may be fractional.
