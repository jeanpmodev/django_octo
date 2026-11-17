import os
import re
import time
import requests

API_KEY = os.environ["PEPY_API_KEY"]

PACKAGES = [
    {"pypi": "django-octo", "repo": "django_octo"},
    {"pypi": "django-octo-seo", "repo": "django_octo_seo"},
    {"pypi": "django-octo-security", "repo": "django_octo_security"},
    {"pypi": "django-octo-aurora", "repo": "django_octo_aurora"},
    {"pypi": "django-octo-uml", "repo": "django_octo_uml"},
    {"pypi": "octo-qa", "repo": "octo_qa"},
]

GITHUB_USER = "jeanpmodev"
headers = {"X-API-Key": API_KEY}
rows = []
total_downloads = 0

for pkg in PACKAGES:
    pypi_name = pkg["pypi"]
    repo_name = pkg["repo"]
    url = f"https://pepy.tech{pypi_name}"

    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    downloads = data.get("total_downloads", 0)
    versions = data.get("versions", [])
    latest_version = versions[-1] if versions else "N/A"
    total_downloads += downloads

    downloads_fmt = f"{downloads:,}"

    repo_link = f"[{pypi_name}](https://github.com{GITHUB_USER}/{repo_name})"
    pepy_link = f"[{downloads_fmt}](https://pepy.tech{pypi_name})"

    rows.append(f"| {repo_link} | `{latest_version}` | {pepy_link} |")

    time.sleep(15)

total_fmt = f"{total_downloads:,}"

table = [
    "| Package | Latest Version | Total Downloads |",
    "| :--- | :---: | ---: |",
    *rows,
    f"| **Ecosystem Total** | — | **{total_fmt}** |",
]

new_content = "\n".join(table)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

pattern = r"(<!-- START_STATS -->).*?(<!-- END_STATS -->)"
updated_readme = re.sub(
    pattern,
    rf"\1\n{new_content}\n\2",
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated_readme)
