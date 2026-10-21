import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ClusterNames(unittest.TestCase):
    def test_dropdowns(self):
        dashboard = json.loads((ROOT / "contour-ingress-metrics.json").read_text())
        variables = {v["name"]: v for v in dashboard["templating"]["list"]}
        for cluster, namespace, service in [
            ("foo-bar-123_api-v2_8080", "foo-bar-123", "api-v2"),
            ("foo-bar_api_80", "foo-bar", "api"),
            ("team9_v2-api_8443", "team9", "v2-api"),
        ]:
            for name, expected in [("namespace", namespace), ("service", service)]:
                with self.subTest(cluster=cluster, variable=name):
                    match = re.fullmatch(variables[name]["regex"], cluster)
                    self.assertIsNotNone(match)
                    self.assertEqual(match[1], expected)

    def test_label_replacement_patterns(self):
        count = 0
        for filename in ["contour-ingress-metrics.json", "contour-global-metrics.json"]:
            dashboard = json.loads((ROOT / filename).read_text())
            for panel in dashboard["panels"]:
                for target in panel.get("targets", []):
                    patterns = re.findall(r'"envoy_cluster_name",\s*("(?:\\.|[^"\\])*")', target.get("expr", ""))
                    for quoted in patterns:
                        pattern = json.loads(quoted)
                        for cluster in ["foo-bar-123_api-v2_8080", "foo-bar_api_80", "team9_v2-api_8443"]:
                            self.assertIsNotNone(re.fullmatch(pattern, cluster), (filename, panel["id"], pattern, cluster))
                        count += 1
        self.assertGreater(count, 0)

if __name__ == "__main__":
    unittest.main()
