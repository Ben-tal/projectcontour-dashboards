"""Local-only dashboard edits for the Minikube demo stack."""

DATASOURCE_UID = "yesodot-devs"
REPLACEMENTS = {
    "${VAR_SERVICE}": "contour-envoy-metrics",
    "ingress_https": "ingress_(http|https)",
}


def replace_placeholders(value):
    if isinstance(value, dict):
        return {key: replace_placeholders(item) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_placeholders(item) for item in value]
    if isinstance(value, str):
        if value.startswith("${DS_") and value.endswith("}"):
            value = "${datasource}"
        for source, target in REPLACEMENTS.items():
            value = value.replace(source, target)
    return value


def set_local_defaults(dashboard):
    """Select the Contour and sample-app labels emitted by local Prometheus."""
    for variable in dashboard.get("templating", {}).get("list", []):
        name = variable.get("name")
        if name == "datasource":
            variable["current"] = {"text": DATASOURCE_UID, "value": DATASOURCE_UID}
        elif name == "contour_namespace":
            variable["current"] = {"text": "projectcontour", "value": "projectcontour"}
        elif name == "namespace" and dashboard.get("title", "").lower().find("ingress") >= 0:
            variable["current"] = {"text": ["contour-test"], "value": ["contour-test"]}
        elif name == "namespace":
            variable["current"] = {"text": "projectcontour", "value": "projectcontour"}
        elif name == "service" and dashboard.get("title", "").lower().find("ingress") >= 0:
            variable["current"] = {
                "text": "All",
                "value": ["$__all"],
            }
    return dashboard
