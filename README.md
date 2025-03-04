# 🚀 [Contour Ingress Metrics Dashboard](https://grafana.com/grafana/dashboards/21396-contour-ingress-metrics/)

## 📌 Overview
The [contour-ingress-metrics](./contour-ingress-metrics.json) Grafana dashboard comprehensively monitors the Project Contour Ingress Controller at the service level, offering a detailed view of various service-level statistics. The dashboard is designed to help you understand the performance, availability, and overall health of your ingress resources.

## 📊 Dashboard Sections

### 1️⃣ Overview
- 📈 **Requests (period)**: Displays the total number of ingress requests over a specific period.
- 🔗 **Connections (period)**: Shows the total number of active connections during the period.
- ✅ **% Success (period)**: Percentage of successful requests over the period.
- ⏳ **Requests (5m)**: Number of requests received in the last 5 minutes.
- 🔄 **Connections (5m)**: Number of connections in the last 5 minutes.
- 📊 **% Success (5m)**: Success rate of requests in the last 5 minutes.
- 🛠 **HTTP Status Codes (5m)**: Breakdown of HTTP status codes (1xx, 2xx, 3xx, 4xx, 5xx) for the last 5 minutes.

### 2️⃣ Request Information
- 🎯 **Ingress Success Requests (non 4|5xx Responses)**: Rate of successful ingress requests.
- ❌ **Ingress Failed Requests (4|5xx Responses)**: Rate of failed ingress requests.
- 📏 **Ingress Success Rate (non-4|5xx Responses)**: Success rate of ingress requests excluding 4xx and 5xx responses.

### 3️⃣ Service Summary
- 🚦 **Ingress**: Overall ingress metrics.
- 📊 **Requests Per Second**: Rate of incoming requests per second.
- 🔄 **Connections Per Second**: Rate of active connections per second.
- ⏳ **Latency (P50, P90, P99)**: Latency metrics at 50th, 90th, and 99th percentiles.

### 4️⃣ Throughput
- 📡 **Upstream Network Traffic**: Network traffic to upstream services.

### 5️⃣ Requests
- 📌 **Total Active Requests**: Current active requests being processed.
- 🆕 **New Requests**: Rate of new requests coming in.
- 📊 **Ingress Request Volume**: Volume of ingress requests over time.

### 6️⃣ Connections
- 🔗 **Total Active Connections**: Number of active connections.
- 🚀 **New Connections**: Rate of new connections being established.
- 📡 **Ingress Connection Volume**: Volume of connections over time.

# 🌍 [Contour Global Metrics](https://grafana.com/grafana/dashboards/21402-contour-global-metrics/)
A Dashboard that monitors general statistics for Contour Ingress Controller (Projectcontour)

## 📌 Overview
The [contour-global-metrics](./contour-global-metrics.json) monitors general and more global statistics for Contour Ingress Controller. It displays real-time metrics for requests, connections, memory usage, and node status to help maintain and optimize performance.

## 🔥 Features
- 📈 **Requests Per Second (RPS)**
- ✅ **Active Requests**
- 🔄 **Connections Per Second (CPS)**
- 🔗 **Active Connections**
- 💾 **Memory Usage**
- 🖥 **Node Status**
- 🔍 **HTTPProxy Resource Status**
