import importlib.util
from django.urls import include, path
from . import discover_octo_modules
from .views import octo_hub_view

CUSTOM_PREFIXES = {
    "django_octo_seo": "seo-demo/",
}

urlpatterns = [
    path("octo/", octo_hub_view, name="django_octo_hub"),
]

for module_name in discover_octo_modules():
    if importlib.util.find_spec(f"{module_name}.urls") is not None:
        prefix = CUSTOM_PREFIXES.get(module_name, "")
        urlpatterns.append(path(prefix, include(f"{module_name}.urls")))