"""Execute the dashboard's actual success queries against synthetic Prometheus series.

Requires promtool on PATH. Run: python tests/test_success_rates.py
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def suite():
    dashboard = json.loads((ROOT / "contour-ingress-metrics.json").read_text())
    expressions = {}
    for panel in dashboard["panels"]:
        if panel["id"] in [18, 28, 30]:
            expressions[panel["id"]] = (panel["targets"][0]["expr"]
                .replace("${contour_namespace}", "projectcontour")
                .replace("${namespace}", "foo-bar-123")
                .replace("${service}", "api-v2")
                .replace("${__range_s}", "300"))
    assert len(expressions) == 3
    # port, response code, counter increment per minute
    cases = [
        ("healthy two ports", [(80,200,100),(8080,200,100)], 1.0),
        ("unequal traffic weights", [(80,200,90),(80,500,10),(8080,500,900)], 0.09),
        ("404 excluded", [(80,200,90),(80,500,10),(80,404,900)], 0.9),
        ("all failures without a success series", [(80,500,100),(8080,503,200)], 0.0),
        ("only 404 has no eligible traffic", [(80,404,100)], None),
    ]
    tests = []
    for name, inputs, expected in cases:
        series = []
        for port, code, increment in inputs:
            series.append({"series": 'envoy_cluster_upstream_rq{namespace="projectcontour", envoy_cluster_name="foo-bar-123_api-v2_%d", envoy_response_code="%d"}' % (port, code),
                           "values": "0+%sx10" % increment})
        # A second controller exporting the same cluster must not affect this result.
        series.append({"series": 'envoy_cluster_upstream_rq{namespace="other-contour", envoy_cluster_name="foo-bar-123_api-v2_80", envoy_response_code="500"}', "values":"0+99999x10"})
        checks = []
        for panel_id, expr in expressions.items():
            labels = '{ingress="foo-bar-123/api-v2"}' if panel_id == 30 else '{}'
            checks.append({"expr":expr, "eval_time":"10m", "exp_samples": [] if expected is None else [{"labels": labels, "value":expected}]})
        tests.append({"name":name, "interval":"1m", "input_series":series, "promql_expr_test":checks})
    return {"rule_files":[], "evaluation_interval":"1m", "tests":tests}

if __name__ == "__main__":
    promtool = shutil.which("promtool")
    if not promtool:
        raise SystemExit("promtool is required; no Prometheus evaluation has been run")
    with tempfile.TemporaryDirectory() as directory:
        fixture = Path(directory) / "success.test.yml"
        fixture.write_text(json.dumps(suite(), indent=2))
        subprocess.run([promtool, "test", "rules", str(fixture)], check=True)
