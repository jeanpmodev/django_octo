import importlib.metadata
import importlib.util
from django.conf import settings

__version__ = "0.1.15"

OCTO_MODULES = [
    "django_octo_seo",
    "django_octo_security",
    "django_octo_uml",
    "django_octo_qa",
    "django_octo_aurora",
]


def discover_octo_modules() -> list[str]:
    """Discover all installed django_octo_* satellites and third-party plugins."""
    discovered: set[str] = {
        mod for mod in OCTO_MODULES if importlib.util.find_spec(mod) is not None
    }

    for dist in importlib.metadata.distributions():
        pkg_name = dist.metadata.get("Name", "")
        normalized = pkg_name.lower().replace("-", "_")
        if normalized.startswith("django_octo_") and normalized != "django_octo":
            if importlib.util.find_spec(normalized) is not None:
                discovered.add(normalized)

    for ep in importlib.metadata.entry_points(group="django_octo.plugins"):
        if importlib.util.find_spec(ep.value) is not None:
            discovered.add(ep.value)

    return sorted(discovered)


def get_installed_octo_apps() -> list[str]:
    """Auto-discovers installed Django-Octo satellite modules at build/runtime."""
    return ["django_octo", *discover_octo_modules()]


def _auto_inject_installed_apps() -> None:
    """Ensure all detected satellites are registered when only 'django_octo' is listed."""
    if not settings.configured:
        return
    current_apps = list(settings.INSTALLED_APPS)
    added = False
    for mod in discover_octo_modules():
        if mod not in current_apps:
            current_apps.append(mod)
            added = True
    if added:
        settings.INSTALLED_APPS = current_apps


_auto_inject_installed_apps()
