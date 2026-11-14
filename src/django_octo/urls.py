import importlib.util
from django.urls import include, path
from .views import octo_hub_view

urlpatterns = [
    path("octo/", octo_hub_view, name="django_octo_hub"),
]

if importlib.util.find_spec("django_octo_seo") is not None:
    urlpatterns.append(path("seo-demo/", include("django_octo_seo.urls")))

if importlib.util.find_spec("django_octo_security") is not None:
    urlpatterns.append(path("", include("django_octo_security.urls")))
