"""
Daily sync: checks Kaggle for newly-public notebooks/datasets and appends
a card for each one to the #kaggle section of index.html.

State is tracked in scripts/kaggle_sync_state.json (refs already on the site).
Requires the Kaggle CLI to be authenticated (kaggle config view).
"""
import json
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = REPO_ROOT / "scripts" / "kaggle_sync_state.json"
INDEX_FILE = REPO_ROOT / "index.html"
GRID_MARKER = '<div class="courses-grid fade-in" id="kaggleGrid">'


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}\n{result.stderr}", file=sys.stderr)
        return None
    return result.stdout


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"known_refs": []}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def list_kernel_refs():
    out = run(["kaggle", "kernels", "list", "--mine", "--csv"])
    if not out:
        return []
    lines = out.strip().splitlines()[1:]
    return [line.split(",")[0] for line in lines if line.strip()]


def list_dataset_refs():
    out = run(["kaggle", "datasets", "list", "--mine", "--csv"])
    if not out or "No datasets found" in out:
        return []
    lines = out.strip().splitlines()[1:]
    return [line.split(",")[0] for line in lines if line.strip()]


def get_kernel_metadata(ref):
    tmpdir = tempfile.mkdtemp()
    try:
        run(["kaggle", "kernels", "pull", ref, "-p", tmpdir, "-m"])
        meta_path = Path(tmpdir) / "kernel-metadata.json"
        if not meta_path.exists():
            return None
        return json.loads(meta_path.read_text())
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def get_dataset_metadata(ref):
    owner, slug = ref.split("/", 1)
    tmpdir = tempfile.mkdtemp()
    try:
        run(["kaggle", "datasets", "metadata", ref, "-p", tmpdir])
        meta_path = Path(tmpdir) / "dataset-metadata.json"
        if not meta_path.exists():
            return None
        return json.loads(meta_path.read_text())
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def build_card(title, url, kind, date_str):
    return f'''
            <div class="course-card">
                <div class="course-provider">{kind}</div>
                <div class="course-name">{title}</div>
                <div class="course-meta">Kaggle · {date_str}</div>
                <div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;">
                    <div class="course-badge done">Public</div>
                    <a href="{url}" target="_blank" style="font-size:12px;color:var(--accent);text-decoration:none;font-family:var(--font-mono);letter-spacing:0.04em;">View ↗</a>
                </div>
            </div>
'''


def insert_cards(cards_html):
    content = INDEX_FILE.read_text(encoding="utf-8")
    idx = content.index(GRID_MARKER) + len(GRID_MARKER)
    new_content = content[:idx] + cards_html + content[idx:]
    INDEX_FILE.write_text(new_content, encoding="utf-8")


def main():
    state = load_state()
    known = set(state["known_refs"])

    new_cards = []
    new_refs = []

    for ref in list_kernel_refs():
        if ref in known:
            continue
        meta = get_kernel_metadata(ref)
        if not meta or meta.get("is_private", True):
            continue
        title = meta.get("title", ref)
        date_str = "recently published"
        url = f"https://www.kaggle.com/code/{ref}"
        new_cards.append(build_card(title, url, "Notebook", date_str))
        new_refs.append(ref)

    for ref in list_dataset_refs():
        if ref in known:
            continue
        meta = get_dataset_metadata(ref)
        if not meta or meta.get("isPrivate", meta.get("is_private", True)):
            continue
        title = meta.get("title", ref)
        date_str = "recently published"
        url = f"https://www.kaggle.com/datasets/{ref}"
        new_cards.append(build_card(title, url, "Dataset", date_str))
        new_refs.append(ref)

    if not new_cards:
        print("No new public Kaggle notebooks/datasets found.")
        return

    insert_cards("".join(new_cards))
    state["known_refs"] = list(known | set(new_refs))
    save_state(state)

    print(f"Added {len(new_cards)} new card(s) for: {', '.join(new_refs)}")
    print("NEW_ITEMS_ADDED")


if __name__ == "__main__":
    main()
