import importlib.metadata
import importlib.util
from typing import Any

CORE_MODULE = "django_octo"

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
    {
        "package": "django-octo-uml",
        "module": "django_octo_uml",
        "title": "Automated UML Entity & Architecture Mapper",
        "layer": "Live Schema & Relationship Introspection",
        "description": "Zero-config entity relationship and architecture visualizer inspecting all registered Django apps.",
        "public_url": None,
        "admin_url": "/admin/",
    },
    {
        "package": "django-octo-qa",
        "module": "django_octo_qa",
        "title": "Unified Quality Assurance Orchestrator",
        "layer": "Pytest, Behave BDD & Locust Execution Hub",
        "description": "Granular test discovery and on-demand execution runner with persistent history in Django Admin.",
        "public_url": None,
        "admin_url": "/admin/",
    },
]


def discover_octo_modules() -> list[str]:
    """Return all installed django_octo_* modules and third-party entry-point plugins."""
    discovered: set[str] = {
        item["module"]
        for item in MODULE_CATALOG
        if importlib.util.find_spec(item["module"]) is not None
    }

    for dist in importlib.metadata.distributions():
        pkg_name = dist.metadata.get("Name", "")
        normalized = pkg_name.lower().replace("-", "_")
        if normalized.startswith("django_octo_") and normalized != CORE_MODULE:
            if importlib.util.find_spec(normalized) is not None:
                discovered.add(normalized)

    for ep in importlib.metadata.entry_points(group="django_octo.plugins"):
        if importlib.util.find_spec(ep.value) is not None:
            discovered.add(ep.value)

    return sorted(discovered)


def discover_octo_ecosystem() -> dict[str, Any]:
    """Inspects the active runtime environment and builds live module telemetry."""
    try:
        core_version = importlib.metadata.version("django-octo")
    except importlib.metadata.PackageNotFoundError:
        core_version = "0.2.0-dev"

    catalog_by_module = {item["module"]: item for item in MODULE_CATALOG}
    all_detected_modules = sorted(
        set(catalog_by_module.keys()) | set(discover_octo_modules())
    )

    modules_status = []
    active_count = 0

    for mod_name in all_detected_modules:
        base_meta = catalog_by_module.get(
            mod_name,
            {
                "package": mod_name.replace("_", "-"),
                "module": mod_name,
                "title": mod_name.replace("_", " ").title(),
                "layer": "Auto-Discovered Runtime Extension",
                "description": "Dynamically detected module integrated into the Django-Octo runtime.",
                "public_url": None,
                "admin_url": "/admin/",
            },
        )

        is_installed = importlib.util.find_spec(mod_name) is not None
        version = None
        if is_installed:
            active_count += 1
            try:
                version = importlib.metadata.version(base_meta["package"])
            except importlib.metadata.PackageNotFoundError:
                version = "local-editable"

        modules_status.append({
            **base_meta,
            "installed": is_installed,
            "version": version,
        })

    return {
        "core_version": core_version,
        "active_count": active_count,
        "total_catalog": len(modules_status),
        "modules": modules_status,
    }
