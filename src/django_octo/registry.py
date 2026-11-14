import importlib.metadata
import importlib.util
from typing import Any

MODULE_CATALOG = [
    {
        "package": "django-octo-seo",
        "module": "django_octo_seo",
        "title": "Semantic & SEO Injection Engine",
        "layer": "8-Layer Metadata & Single-Block JSON-LD",
        "description": "High-performance single-query SEO runtime engine optimizing crawlers, Open Graph, and generative AI indexers.",
        "public_url": "/seo-demo/",
        "admin_url": "/admin/",
    },
    {
        "package": "django-octo-security",
        "module": "django_octo_security",
        "title": "Runtime Security & CVE Audit Engine",
        "layer": "Zero-Dependency OSV.dev & HTTP Posture",
        "description": "Non-intrusive Dual-Channel security posture enforcer and real-time virtual environment CVE auditor.",
        "public_url": "/security-audit/",
        "admin_url": "/admin/",
    },
]


def discover_octo_ecosystem() -> dict[str, Any]:
    """Inspects the active runtime environment and builds live module telemetry."""
    try:
        core_version = importlib.metadata.version("django-octo")
    except importlib.metadata.PackageNotFoundError:
        core_version = "0.1.8-dev"

    modules_status = []
    active_count = 0

    for item in MODULE_CATALOG:
        is_installed = importlib.util.find_spec(item["module"]) is not None
        version = None
        if is_installed:
            active_count += 1
            try:
                version = importlib.metadata.version(item["package"])
            except importlib.metadata.PackageNotFoundError:
                version = "local-editable"

        modules_status.append({
            **item,
            "installed": is_installed,
            "version": version,
        })

    return {
        "core_version": core_version,
        "active_count": active_count,
        "total_catalog": len(MODULE_CATALOG),
        "modules": modules_status,
    }
