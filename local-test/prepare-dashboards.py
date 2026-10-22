#!/usr/bin/env python3
"""Prepare repo dashboards for Grafana file provisioning without editing source JSON."""

import json
import pathlib
import sys

from dashboard_helpers import replace_placeholders, set_local_defaults


repo = pathlib.Path(__file__).resolve().parents[1]
output = pathlib.Path(sys.argv[1])
output.mkdir(parents=True, exist_ok=True)

for filename in ("contour-global-metrics.json", "contour-ingress-metrics.json"):
    dashboard = json.loads((repo / filename).read_text(encoding="utf-8"))
    dashboard = set_local_defaults(replace_placeholders(dashboard))
    dashboard.pop("__inputs", None)
    dashboard.pop("__elements", None)
    dashboard["id"] = None
    (output / filename).write_text(
        json.dumps(dashboard, indent=2) + "\n", encoding="utf-8"
    )
