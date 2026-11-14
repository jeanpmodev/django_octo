import os
import sys
from pathlib import Path

# Aponta para o settings da sandbox local ou configura um ambiente mínimo em memória
import django
from django.conf import settings

if not settings.configured:
    from django_octo import get_installed_octo_apps
    settings.configure(
        SECRET_KEY="test-secret-key",
        ROOT_URLCONF="django_octo.urls",
        INSTALLED_APPS=[
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            *get_installed_octo_apps(),
        ],
        TEMPLATES=[{
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
        }],
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    )
    django.setup()

from django.test import Client
from django_octo.registry import discover_octo_ecosystem


def test_ecosystem_auto_discovery():
    data = discover_octo_ecosystem()
    assert data["active_count"] == 2
    assert len(data["modules"]) == 2


def test_octo_hub_endpoint():
    client = Client()
    response = client.get("/octo/")
    assert response.status_code == 200
    assert b"Django-Octo Control Hub" in response.content
