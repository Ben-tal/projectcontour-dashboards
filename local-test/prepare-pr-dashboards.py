#!/usr/bin/env python3
"""Download dashboard JSON changed by PRs #8-14 and prepare Grafana provisioning."""

import base64
import json
import pathlib
import subprocess
import sys
import urllib.parse

from dashboard_helpers import replace_placeholders, set_local_defaults

REPOSITORY = "Ben-tal/projectcontour-dashboards"
PR_NUMBERS = range(8, 15)
DASHBOARD_FILES = {
    "contour-global-metrics.json",
    "contour-ingress-metrics.json",
}
def gh_json(endpoint):
    result = subprocess.run(
        ["gh", "api", endpoint], check=True, capture_output=True, text=True
    )
    return json.loads(result.stdout)


def main():
    output = pathlib.Path(sys.argv[1])
    providers_manifest = pathlib.Path(sys.argv[2])
    output.mkdir(parents=True, exist_ok=True)
    providers = []
    summaries = []

    for number in PR_NUMBERS:
        pull = gh_json(f"repos/{REPOSITORY}/pulls/{number}")
        changed_files = gh_json(
            f"repos/{REPOSITORY}/pulls/{number}/files?per_page=100"
        )
        folder = f"Draft PR #{number} - {pull['title']}" if pull["draft"] else (
            f"PR #{number} - {pull['title']}"
        )
        directory_name = f"pr-{number}"
        dashboard_dir = output / directory_name
        dashboard_dir.mkdir(parents=True, exist_ok=True)
        prepared_count = 0

        for changed in changed_files:
            filename = changed["filename"]
            if filename not in DASHBOARD_FILES or changed["status"] == "removed":
                continue

            encoded_path = urllib.parse.quote(filename, safe="/")
            content = gh_json(
                f"repos/{REPOSITORY}/contents/{encoded_path}?ref={pull['head']['sha']}"
            )
            dashboard = json.loads(base64.b64decode(content["content"]))
            dashboard = set_local_defaults(replace_placeholders(dashboard))
            dashboard.pop("__inputs", None)
            dashboard.pop("__elements", None)
            dashboard["id"] = None
            dashboard["uid"] = f"pr{number}-{pathlib.Path(filename).stem}"
            dashboard["title"] = f"{dashboard.get('title', pathlib.Path(filename).stem)} (PR #{number})"
            (dashboard_dir / pathlib.Path(filename).name).write_text(
                json.dumps(dashboard, indent=2) + "\n", encoding="utf-8"
            )
            prepared_count += 1

        if not prepared_count:
            raise RuntimeError(f"PR #{number} has no changed Contour dashboard JSON")

        providers.append(
            {
                "name": directory_name,
                "orgId": 1,
                "folder": folder,
                "folderUid": f"contour-pr-{number}",
                "type": "file",
                "disableDeletion": True,
                "editable": False,
                "options": {"path": f"/var/lib/grafana/dashboards/{directory_name}"},
            }
        )
        summaries.append(f"PR #{number}: {prepared_count} dashboard(s) -> {folder}")

    provider_config = {"apiVersion": 1, "providers": providers}
    manifest = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": "grafana-pr-dashboard-provisioning",
            "namespace": "contour-test",
        },
        "data": {"prs.yaml": json.dumps(provider_config, indent=2)},
    }
    providers_manifest.parent.mkdir(parents=True, exist_ok=True)
    providers_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("\n".join(summaries))


if __name__ == "__main__":
    main()
