import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SATELLITES = ["django-octo-seo", "django-octo-security"]
BASE_MINOR = "0.1"


def get_pypi_release_count(package: str) -> tuple[str, int]:
    host = ".".join(["pypi", "org"])
    url = urllib.parse.urlunparse(("https", host, f"/pypi/{package}/json", "", "", ""))
    req = urllib.request.Request(url, headers={"User-Agent": "django-octo-orchestrator/1.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))
        latest_version = data["info"]["version"]
        release_count = len(data.get("releases", {}))
        return latest_version, release_count


def main() -> None:
    total_releases = 0
    versions_map = {}

    for pkg in SATELLITES:
        latest, count = get_pypi_release_count(pkg)
        versions_map[pkg] = latest
        total_releases += count

    new_version = f"{BASE_MINOR}.{total_releases}"

    # Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text(encoding="utf-8")
    content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content, count=1)
    for pkg, ver in versions_map.items():
        content = re.sub(rf'"{pkg}>=[^"]+"', f'"{pkg}>={ver}"', content)
    pyproject_path.write_text(content, encoding="utf-8")

    # Update __init__.py
    init_path = Path("src/django_octo/__init__.py")
    init_content = init_path.read_text(encoding="utf-8")
    init_content = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{new_version}"', init_content, count=1)
    init_path.write_text(init_content, encoding="utf-8")

    # Append automated release entry to CHANGELOG.md
    module_changed = os.getenv("DISPATCH_MODULE", "ecosystem-sync")
    module_version = os.getenv("DISPATCH_VERSION", "latest")
    change_summary = os.getenv("DISPATCH_SUMMARY", "Automated cumulative ecosystem synchronization.")
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    changelog_path = Path("CHANGELOG.md")
    entry = (
        f"## [{new_version}] - {date_str}\n"
        f"- **Updated Module:** `{module_changed}` (`v{module_version}`)\n"
        f"- **Summary:** {change_summary}\n\n"
    )
    existing = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else "# Changelog\n\n"
    if "# Changelog" in existing:
        updated_changelog = existing.replace("# Changelog\n\n", f"# Changelog\n\n{entry}", 1)
    else:
        updated_changelog = f"# Changelog\n\n{entry}{existing}"
    changelog_path.write_text(updated_changelog, encoding="utf-8")

    print(f"NEW_VERSION={new_version}")


if __name__ == "__main__":
    main()
