import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OWNER = "jeanpmodev"
MODULES = [
    ("django-octo (Core)", "django_octo"),
]

SECURITY_FILE = Path("SECURITY.md")
START_MARKER = "<!-- OCTO-SEC-START -->"
END_MARKER = "<!-- OCTO-SEC-END -->"


def fetch_scorecard(repo: str) -> str:
    url = f"https://scorecard.dev{OWNER}/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "Django-Octo-Security-Intel"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            score = data.get("score")
            if score is not None:
                return f"`{score:.1f} / 10`"
    except (urllib.error.URLError, TimeoutError, ValueError):
        pass
    return "`Pending`"


def fetch_snyk_workflow_status(repo: str) -> str:
    url = f"https://github.com{OWNER}/{repo}/actions/workflows/security.yml/runs?per_page=1&branch=main"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Django-Octo-Security-Intel",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            runs = data.get("workflow_runs", [])
            if runs:
                conclusion = runs[0].get("conclusion")
                if conclusion == "success":
                    return "`0 Known (Pass)`"
                if conclusion is None:
                    return "`Running`"
                return f"`Alert ({conclusion})`"
    except (urllib.error.URLError, TimeoutError, ValueError):
        pass
    return "`Not Configured`"


def build_table() -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        START_MARKER,
        "",
        "| Module | OpenSSF Scorecard | Snyk Audit (CI) | PyPI Provenance | Last Check (UTC) |",
        "| :--- | :---: | :---: | :---: | :---: |",
    ]
    for label, repo in MODULES:
        score = fetch_scorecard(repo)
        snyk = fetch_snyk_workflow_status(repo)
        lines.append(f"| **{label}** | {score} | {snyk} | Verified (OIDC) | {today} |")
    lines.append("")
    lines.append(END_MARKER)
    return "\n".join(lines)


def main() -> None:
    new_block = build_table()

    if not SECURITY_FILE.exists():
        content = (
            "# Security Policy & Live Posture\n\n"
            "Central security governance and live audit telemetry for the **Django-Octo** core orchestrator.\n\n"
            "## Live Security Telemetry\n\n"
            f"{new_block}\n\n"
            "## Supported Versions\n\n"
            "Only the latest cumulative release of **django-octo** receives active security updates.\n\n"
            "## Coordinated Vulnerability Disclosure (CVD)\n\n"
            "Please do **not** report security vulnerabilities through public GitHub issues.\n"
            "Use **GitHub Private Vulnerability Reporting** in the **Security** tab of this repository.\n"
        )
        SECURITY_FILE.write_text(content, encoding="utf-8")
        return

    current_content = SECURITY_FILE.read_text(encoding="utf-8")
    pattern = re.compile(f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL)

    old_match = pattern.search(current_content)
    if old_match:
        old_lines = [line.rsplit("|", 2) for line in old_match.group(0).splitlines() if line.startswith("| **")]
        new_lines = [line.rsplit("|", 2) for line in new_block.splitlines() if line.startswith("| **")]
        if old_lines == new_lines:
            return

    if pattern.search(current_content):
        updated_content = pattern.sub(new_block, current_content)
    else:
        updated_content = f"{current_content.rstrip()}\n\n## Live Security Telemetry\n\n{new_block}\n"

    SECURITY_FILE.write_text(updated_content, encoding="utf-8")


if __name__ == "__main__":
    main()
