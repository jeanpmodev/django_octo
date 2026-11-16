from django.apps import AppConfig, apps
from django.conf import settings
from . import discover_octo_modules


class DjangoOctoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_octo"
    verbose_name = "Django-Octo Core Orchestrator"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self._inject_satellite_apps()

    def _inject_satellite_apps(self) -> None:
        current_apps = list(settings.INSTALLED_APPS)
        added = False

        for module_name in discover_octo_modules():
            if module_name not in current_apps:
                current_apps.append(module_name)
                added = True

        if added:
            settings.INSTALLED_APPS = current_apps
            if apps.loading:
                apps.populate(settings.INSTALLED_APPS)
