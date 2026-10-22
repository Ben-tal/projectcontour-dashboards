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

## Import and configure the dashboards

These instructions use an existing Contour installation, Prometheus, and Grafana. The dashboards require Contour and Envoy metrics; importing JSON does not configure scraping.

1. Configure Prometheus to scrape Contour's `/metrics` endpoint and Envoy's `/stats/prometheus` endpoint. Check that both targets are **UP** in Prometheus. The [example scrape configuration](./docs/prometheus-example.yaml) uses the Contour quickstart's `app=contour` and `app=envoy` pod labels, ports 8000 and 8002, and the `projectcontour` namespace. Adapt these selectors, ports, and namespace to your deployment. Prometheus must have Kubernetes permissions to get, list, and watch the selected pods.
2. Add a **Prometheus** datasource in Grafana. Its URL must be reachable from the Grafana server, for example `http://prometheus.monitoring.svc:9090` when that Kubernetes service exists. Save and test the datasource, then set its **Scrape interval** to the actual Prometheus scrape interval. The example uses 15 seconds. If you scrape Envoy every 60 seconds, configure 60 seconds here as well. A query's **Min step**, when set, overrides the datasource interval used by `$__rate_interval`.
3. In Grafana, choose **Dashboards → New → Import** and upload [contour-ingress-metrics.json](./contour-ingress-metrics.json), then [contour-global-metrics.json](./contour-global-metrics.json). Select your Prometheus datasource in each dashboard's **datasource** dropdown; do not assume a saved datasource UID exists in your Grafana instance.
4. During the global dashboard import, set the **Service** input to the scrape `service` label value on both Contour and Envoy metrics. The example sets it to `contour-envoy-metrics`. This is a scrape label, not the name of an application backend. For file provisioning, substitute `${VAR_SERVICE}` with your label value before provisioning the JSON; Grafana's file provisioner does not display the import-input form.
5. In the global dashboard, select the controller's scrape **Namespace**. In the ingress dashboard, the hidden **Contour Namespace** must identify the same controller scrape namespace; use a URL parameter such as `var-contour_namespace=projectcontour` if you need to change it. Then select an application **Namespace** and **Service**, populated from `envoy_cluster_name`.
6. Generate requests through a configured HTTPProxy or Ingress hostname, for example `curl -H 'Host: app.example.test' http://127.0.0.1:8080/` when port 8080 is forwarded to your Envoy HTTP service. Use the hostname and port for your route. Wait for at least two scrapes before checking counter rates. Longer windows provide more stable results.
7. Open **Upstream Cluster Drilldown** in the global dashboard and select an ingress namespace or service. Keep the ingress dashboard UID `b1b27299-bed8-4982-ab03-f0c79ccef5fc` when importing so its data links resolve. If you change that UID or host the dashboards in separate Grafana organizations, update the table's data links. The link passes the datasource, controller scrape namespace, application namespace/service, and selected time range.

For `$__rate_interval`, Grafana uses the larger of `$__interval + scrape_interval` and `4 × scrape_interval`. This helps `rate` and `irate` receive enough samples; it does not create missing metrics. See [Grafana's Prometheus variables documentation](https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/#use-__rate_interval).

### Scrape labels and application names

| Value | Meaning | Example |
| --- | --- | --- |
| Metric label `namespace` | Kubernetes namespace of the controller/Envoy scrape target | `projectcontour` |
| Metric label `service` | Label identifying the controller's metrics scrape service; configured by relabeling or your ServiceMonitor | `contour-envoy-metrics` |
| Metric label `pod` | Envoy pod name; needed to distinguish rows in **Node State per Pod** | `envoy-abc12` |
| Label `envoy_cluster_name` | Backend cluster name from Envoy; parsed into application namespace, service, and port | `team-1_backend-2_8080` |
| Ingress dashboard variable `namespace` | Application namespace extracted from the cluster name | `team-1` |
| Ingress dashboard variable `service` | Application backend service extracted from the cluster name | `backend-2` |

The Envoy metric above still has scrape labels `namespace="projectcontour"` and `service="contour-envoy-metrics"`. Neither becomes `team-1` or `backend-2`. Keep each target's distinct `instance` label, which Prometheus normally supplies, so multiple replicas remain separate before aggregation. `envoy_response_code`, `envoy_response_code_class`, `envoy_http_conn_manager_prefix`, and histogram `le` labels must also survive any metric relabeling.

The sample configuration sets `namespace`, `service`, and `pod` through relabeling. It assumes the quickstart's pod labels and metrics endpoints; it is not a complete Prometheus Kubernetes installation or an RBAC manifest. With the Prometheus Operator, configure equivalent target labels in the relevant PodMonitor or ServiceMonitor rather than adding a second scrape of the same targets. See [Prometheus configuration and relabeling](https://prometheus.io/docs/prometheus/latest/configuration/configuration/).

### Required metrics

Check the names actually exported by your Contour/Envoy version. The dashboards expect these families directly; no recording rules are required:

| Source | Metric families used |
| --- | --- |
| Contour | `contour_build_info`, `contour_httpproxy`, `contour_httpproxy_valid`, `contour_httpproxy_invalid` |
| Envoy process and runtime | `envoy_server_live`, `envoy_server_state`, `envoy_server_uptime`, `envoy_server_memory_physical_size`, and `envoy_runtime_update_attempt`, `envoy_runtime_update_failure`, `envoy_runtime_update_rejected`, `envoy_runtime_update_success` |
| Envoy upstream clusters | `envoy_cluster_update_time`, `envoy_cluster_membership_healthy`, `envoy_cluster_upstream_rq_total`, `envoy_cluster_upstream_rq`, `envoy_cluster_upstream_rq_xx`, `envoy_cluster_upstream_rq_active`, `envoy_cluster_upstream_rq_time_bucket`, `envoy_cluster_upstream_cx_total`, `envoy_cluster_upstream_cx_active`, `envoy_cluster_upstream_cx_rx_bytes_total`, `envoy_cluster_upstream_cx_tx_bytes_total` |
| Envoy downstream HTTP | `envoy_http_downstream_rq_total`, `envoy_http_downstream_rq_active`, `envoy_http_downstream_cx_total`, `envoy_http_downstream_cx_active`, `envoy_http_downstream_cx_rx_bytes_total`, `envoy_http_downstream_cx_tx_bytes_total` |

The ingress selectors expect cluster names in `namespace_service_numeric-port` form. Request-code series may appear only after that response code has occurred. A valid route with successful requests does not guarantee that 404/503 series already exist.

### Verified environment and compatibility limits

The local review used this specific environment:

| Component | Observed version |
| --- | --- |
| Grafana | 13.2.4 |
| Prometheus and promtool | 3.5.0 |
| Contour | 1.33.7 |
| Envoy | 1.38.4 |

Both dashboards were loaded into Grafana and their queries checked against live Contour/Envoy metrics. The example scrape configuration was checked with promtool, and Kubernetes discovery/relabeling was checked against the running Contour and Envoy pods. These checks cover this environment, not a compatibility matrix or every possible runtime event. Version strings embedded in exported panel metadata do not establish a minimum supported Grafana version. Other versions may work if they provide the same metric families, labels, and Grafana features; verify those rather than assuming compatibility.

### Troubleshooting empty or unexpected panels

- **Everything is empty:** use the datasource dropdown to select the configured Prometheus datasource, check its connection, and check Prometheus **Targets**. In Explore, run `contour_build_info` and `envoy_server_live` without dashboard filters.
- **Unfiltered metrics work but the dashboard is empty:** inspect the actual `namespace` and `service` metric labels. Match the global Namespace/Service settings and ingress Contour Namespace to those scrape labels, not to your application names.
- **Application dropdowns are empty:** check `envoy_cluster_update_time{namespace="projectcontour"}` with your controller namespace. Confirm a route exists and cluster names follow `namespace_service_numeric-port`. An exported metric without the expected label cannot populate a dropdown.
- **A raw counter exists but a rate is empty:** inspect `count_over_time(envoy_cluster_upstream_cx_total{namespace="projectcontour"}[5m])`. `rate`, `irate`, and `increase` require at least two samples per series. Set the datasource scrape interval correctly, allow targets time to scrape, and inspect the final interpolated query in Grafana's Query Inspector. Fixed two-minute/five-minute count windows can still be too short for very slow or interrupted scrapes.
- **A connection rate is zero while requests continue:** Envoy can reuse existing upstream connections. `envoy_cluster_upstream_cx_total` counts connection establishments; `envoy_cluster_upstream_cx_active` measures currently active connections, and `envoy_cluster_upstream_rq_total` counts requests.
- **Ingress labels are missing:** inspect `envoy_cluster_name` on the result of `rate(...)` before `label_replace`. `rate` preserves that label. The replacement expects namespace/service names with lowercase letters, digits, and hyphens, followed by a numeric port. The final `sum by (ingress)` intentionally drops the original cluster label after extraction.
- **Node state collapses into one row:** preserve a distinct `pod` scrape label as shown in the example. Grouping by an absent label cannot identify separate Envoy pods.
- **A drilldown selects the wrong service/controller:** confirm both dashboards exist in the same Grafana organization and datasource, preserve the ingress UID, and inspect the data-link parameters. Use Query Inspector to confirm controller scrape labels remain separate from parsed application labels.
- **A recently merged change is missing:** inspect the panel query currently loaded by Grafana. Import or reprovision the JSON from the intended branch; a GitHub merge does not refresh an already imported dashboard. File-provisioned dashboards must be updated through their provisioning source.
