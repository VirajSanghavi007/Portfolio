"""
Daily sync: pulls public repo/star counts from GitHub's official public REST API
(no auth needed for public data) and updates the numbers already present in the
#activity section of index.html.
"""
import json
import re
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = REPO_ROOT / "index.html"
USERNAME = "VirajSanghavi007"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "portfolio-sync-script"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    user = fetch(f"https://api.github.com/users/{USERNAME}")
    repos = fetch(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")

    public_repos = user.get("public_repos", 0)
    followers = user.get("followers", 0)
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)

    content = INDEX_FILE.read_text(encoding="utf-8")
    content = re.sub(r'(id="ghRepos" data-target=")\d+(")', rf"\g<1>{public_repos}\g<2>", content)
    content = re.sub(r'(id="ghStars">)[^<]*(</span>)', rf"\g<1>{total_stars}\g<2>", content)
    content = re.sub(r'(id="ghFollowers">)[^<]*(</span>)', rf"\g<1>{followers}\g<2>", content)
    INDEX_FILE.write_text(content, encoding="utf-8")

    print(f"GitHub synced: public_repos={public_repos} stars={total_stars} followers={followers}")


if __name__ == "__main__":
    main()
