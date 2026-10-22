# Local Kubernetes dashboard test

This test stack runs in a dedicated Minikube profile (`contour-dashboard-test`) and uses no managed cloud infrastructure. It installs Project Contour, a small HTTP echo backend, Prometheus, and Grafana. Grafana uses Prometheus to scrape Contour and Envoy metrics. The existing `minikube` profile is left alone.

## Start

From the repository root:

```sh
gh auth login
./local-test/setup.sh
kubectl -n contour-test port-forward svc/grafana 3000:3000
```

Open <http://localhost:3000> and sign in with `admin` / `contour-test`. The two checked-in dashboards are in **Project Contour**. The setup script also reads PRs #8-14 from GitHub and creates one Grafana folder per PR, including the dashboard JSON files changed on that PR's head branch. Draft PR folders are labeled as drafts. The script needs the GitHub CLI (`gh`) authenticated to `Ben-tal/projectcontour-dashboards`; generated dashboard JSON is prepared in a temporary directory and the source files are not modified. Local-only dashboard defaults select the `yesodot-devs` Prometheus datasource, Contour namespace, and sample backend. A small BusyBox pod sends successful and 503 requests through Envoy every two seconds. An intentionally invalid HTTPProxy also feeds the Contour invalid-resource panels.

To generate Envoy request metrics, use a second terminal:

```sh
kubectl -n projectcontour port-forward svc/envoy 8888:80
curl -H 'Host: dashboards.local' http://127.0.0.1:8888/
```

Prometheus is available with `kubectl -n contour-test port-forward svc/prometheus 9090:9090`.

Prometheus data and Grafana state use ephemeral storage and are lost when their pods are recreated. To remove the test components, run `kubectl delete namespace contour-test`. The Contour installation and Minikube profile are left running.

To stop the dedicated local cluster when finished, run `minikube stop -p contour-dashboard-test`.
