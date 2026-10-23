# [Contour Ingress Metrics Dashboard](https://grafana.com/grafana/dashboards/21396-contour-ingress-metrics/)

## Overview
The [contour-ingress-metrics](./contour-ingress-metrics.json) Grafana dashboard comprehensively monitors the Project Contour Ingress Controller at the service level, offering a detailed view of various service-level statistics. The dashboard is designed to help you understand the performance, availability, and overall health of your ingress resources.

## Dashboard Sections

### 1. Overview
- **Requests (period)**: Displays the total number of ingress requests over a specific period.
- **Connections (period)**: Shows the total number of active connections during the period.
- **% Success (period)**: Percentage of successful requests over the period.
- **Requests (5m)**: Number of requests received in the last 5 minutes.
- **Connections (5m)**: Number of connections in the last 5 minutes.
- **% Success (5m)**: Success rate of requests in the last 5 minutes.
- **HTTP Status Codes (5m)**: Breakdown of HTTP status codes (1xx, 2xx, 3xx, 4xx, 5xx) for the last 5 minutes.

### 2. Request Information
- **Ingress Success Requests (non 4|5xx Responses)**: Rate of successful ingress requests.
- **Ingress Failed Requests (4|5xx Responses)**: Rate of failed ingress requests.
- **Ingress Success Rate (non-4|5xx Responses)**: Success rate of ingress requests excluding 4xx and 5xx responses.

### 3. Service Summary
- **Ingress**: Overall ingress metrics.
- **Requests Per Second**: Rate of incoming requests per second.
- **Connections Per Second**: Rate of active connections per second.
- **Latency (P50, P90, P99)**: Latency metrics at 50th, 90th, and 99th percentiles.

### 4. Throughput
- **Upstream Network Traffic**: Network traffic to upstream services.

### 5. Requests
- **Total Active Requests**: Current active requests being processed.
- **New Requests**: Rate of new requests coming in.
- **Ingress Request Volume**: Volume of ingress requests over time.

### 6. Connections
- **Total Active Connections**: Number of active connections.
- **New Connections**: Rate of new connections being established.
- **Ingress Connection Volume**: Volume of connections over time.

## Success-rate policy

The period, five-minute, and per-ingress success percentages use this dashboard policy:

```text
success rate = rate of responses outside 4xx/5xx
               / rate of all responses except 404
```

Rates are summed across the selected service ports before division, so the result is weighted by request volume. The per-ingress chart performs the same aggregation separately for each namespace/service pair. The period statistic uses the selected dashboard range; the five-minute statistic and per-ingress chart use the preceding five minutes.

For example, **90 successful responses, 10 non-404 failures, and 100 responses with status 404 yield 90 / (90 + 10) = 90%**, rather than 90 / 200 = 45%. Eligible traffic containing only failures produces 0%. When no eligible traffic exists, the ratio is undefined (`NaN`) or absent; it does not indicate a successful service. Missing telemetry can also produce no data.

The HTTP status-count and failure-rate panels still include 404 responses. Their totals therefore differ from the success-rate denominator. The **HTTP 1/2xx (5m)** count also excludes 3xx, whereas the success-rate numerator includes 3xx. Dividing that count by all requests will not reproduce the displayed percentage.

Excluding 404 is the dashboard's chosen policy. Applications may classify 404 as a failure differently; this dashboard does not imply that every 404 is harmless.

# [Contour Global Metrics](https://grafana.com/grafana/dashboards/21402-contour-global-metrics/)
A Dashboard that monitors general statistics for Contour Ingress Controller (Projectcontour)

## Overview
The [contour-global-metrics](./contour-global-metrics.json) monitors general and more global statistics for Contour Ingress Controller. It displays real-time metrics for requests, connections, memory usage, and node status to help maintain and optimize performance.

## Features
- Requests Per Second (RPS)
- Active Requests
- Connections Per Second (CPS)
- Active Connections
- Memory Usage
- Node Status
- HTTPProxy Resource Status

## Downstream listener scope

The global dashboard's downstream request and connection counts, rates, active gauges, and network traffic include only `ingress_http` and `ingress_https`. Management connection managers such as `admin` and `stats` are excluded. Upstream panels continue to measure backend cluster traffic.
