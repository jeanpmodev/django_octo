from django.shortcuts import render
from .registry import discover_octo_ecosystem


def octo_hub_view(request):
    """Renders the automated Control Hub documenting all active Django-Octo modules."""
    context = discover_octo_ecosystem()
    return render(request, "django_octo/hub.html", context)
