#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

command -v minikube >/dev/null
command -v kubectl >/dev/null
command -v python3 >/dev/null
command -v gh >/dev/null
gh auth status --hostname github.com >/dev/null

if ! minikube status -p contour-dashboard-test 2>/dev/null | grep -q '^kubelet: Running$'; then
  minikube start -p contour-dashboard-test --driver=docker --cpus=2 --memory=4096
fi
kubectl config use-context contour-dashboard-test
kubectl apply -f https://projectcontour.io/quickstart/contour.yaml
kubectl wait --for=condition=Established --timeout=120s crd/httpproxies.projectcontour.io

python3 "$repo_root/local-test/prepare-dashboards.py" "$tmp_dir/dashboards"
python3 "$repo_root/local-test/prepare-pr-dashboards.py" \
  "$tmp_dir/pr-dashboards" "$tmp_dir/pr-dashboard-provisioning.yaml"
kubectl apply -f "$repo_root/local-test/prometheus.yaml"
kubectl create configmap grafana-dashboards \
  --namespace contour-test \
  --from-file="$tmp_dir/dashboards" \
  --dry-run=client -o yaml | kubectl apply -f -
for pr_dir in "$tmp_dir"/pr-dashboards/pr-*; do
  pr_name="${pr_dir##*/}"
  kubectl create configmap "grafana-${pr_name}-dashboards" \
    --namespace contour-test \
    --from-file="$pr_dir" \
    --dry-run=client -o yaml | kubectl apply -f -
done
kubectl apply -f "$tmp_dir/pr-dashboard-provisioning.yaml"
kubectl apply -f "$repo_root/local-test/grafana.yaml"
kubectl apply -f "$repo_root/local-test/sample-app.yaml"

kubectl -n projectcontour rollout status deployment/contour --timeout=600s
kubectl -n projectcontour rollout status daemonset/envoy --timeout=600s
kubectl -n contour-test rollout status deployment/prometheus --timeout=600s
kubectl -n contour-test rollout status deployment/grafana --timeout=600s
kubectl -n contour-test rollout status deployment/dashboard-sample --timeout=600s
kubectl -n contour-test rollout status deployment/dashboard-failure --timeout=600s
kubectl -n contour-test rollout status deployment/dashboard-traffic --timeout=600s

cat <<'EOF'
Local test stack is ready.

Grafana: kubectl -n contour-test port-forward svc/grafana 3000:3000
Login:   admin / contour-test
Prometheus: kubectl -n contour-test port-forward svc/prometheus 9090:9090
Sample route: kubectl -n projectcontour port-forward svc/envoy 8888:80
Traffic: curl -H 'Host: dashboards.local' http://127.0.0.1:8888/
EOF
