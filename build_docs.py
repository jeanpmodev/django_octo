import pathlib
import re
import urllib.request

REPOS = {
    "index.md": ("django_octo", "Django-Octo Core Orchestrator"),
    "aurora.md": ("django_octo_aurora", "Django-Octo Aurora"),
    "seo.md": ("django_octo_seo", "Django-Octo SEO"),
    "security.md": ("django_octo_security", "Django-Octo Security"),
    "uml.md": ("django_octo_uml", "Django-Octo UML"),
    "qa.md": ("django_octo_qa", "Django-Octo QA"),
}

docs_dir = pathlib.Path("docs")
docs_dir.mkdir(exist_ok=True)

for fname, (repo, explicit_title) in REPOS.items():
    if repo == "django_octo":
        text = pathlib.Path("README.md").read_text(encoding="utf-8")
    else:
        url = f"https://raw.githubusercontent.com/jeanpmodev/{repo}/main/README.md"
        with urllib.request.urlopen(url) as resp:
            text = resp.read().decode("utf-8")

    base = f"https://github.com/jeanpmodev/{repo}/blob/main"
    text = text.replace("(TESTING.md)", f"({base}/TESTING.md)")
    text = text.replace("(LICENSE)", f"({base}/LICENSE)")

    text = re.sub(
        r"^#{1,2}\s+.*pypi library package.*$",
        "",
        text,
        count=1,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    text = re.sub(
        r"(?ms)```mermaid\s*(.*?)\s*```\s*(?:---)?",
        lambda m: f'\n\n<pre class="mermaid"><code>{m.group(1).strip()}</code></pre>\n\n',
        text,
    )

    front_matter = f"---\ntitle: {explicit_title}\n---\n\n"
    (docs_dir / fname).write_text(front_matter + text.lstrip(), encoding="utf-8")
