from django_octo import get_installed_octo_apps
from django_octo.registry import discover_octo_ecosystem


def test_get_installed_octo_apps_includes_core():
    apps = get_installed_octo_apps()
    assert "django_octo" in apps
    assert "django_octo_seo" in apps
    assert "django_octo_security" in apps


def test_ecosystem_auto_discovery():
    data = discover_octo_ecosystem()
    expected_catalog = {
        "django_octo_seo",
        "django_octo_security",
        "django_octo_uml",
        "django_octo_qa",
        "django_octo_aurora",
    }
    discovered_modules = {m["module"] for m in data["modules"]}
    assert expected_catalog <= discovered_modules
    assert data["total_catalog"] >= len(expected_catalog)
    assert data["active_count"] >= 2
