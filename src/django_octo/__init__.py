import importlib.util

__version__ = "0.1.13"

OCTO_MODULES = [
    "django_octo_seo",
    "django_octo_security",
]


def get_installed_octo_apps() -> list[str]:
    """Auto-discovers installed Django-Octo satellite modules at build/runtime."""
    available = ["django_octo"]
    for module in OCTO_MODULES:
        if importlib.util.find_spec(module) is not None:
            available.append(module)
    return available
