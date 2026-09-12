"""
Daily sync: pulls current rating/rank/solved-count from the Codeforces public API
and updates the numbers already present in the #activity section of index.html.

Codeforces has a real public API (no auth needed): api documented at
https://codeforces.com/apiHelp
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = REPO_ROOT / "index.html"
HANDLE = "Black_Water_009"


def fetch(url):
    with urllib.request.urlopen(url, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_info():
    data = fetch(f"https://codeforces.com/api/user.info?handles={HANDLE}")
    if data["status"] != "OK":
        raise RuntimeError(data)
    return data["result"][0]


def get_solved_count():
    data = fetch(f"https://codeforces.com/api/user.status?handle={HANDLE}")
    if data["status"] != "OK":
        raise RuntimeError(data)
    solved = set()
    for sub in data["result"]:
        if sub.get("verdict") == "OK":
            p = sub["problem"]
            solved.add((p.get("contestId"), p.get("index"), p.get("name")))
    return len(solved)


def update_html(rating, rank, solved):
    content = INDEX_FILE.read_text(encoding="utf-8")

    content = re.sub(
        r'(id="cfRating" data-target=")\d+(")',
        rf"\g<1>{rating}\g<2>",
        content,
    )
    content = re.sub(
        r'(id="cfRank">)[^<]*(</span>)',
        rf"\g<1>{rank.title()}\g<2>",
        content,
    )
    content = re.sub(
        r'(id="cfSolved">)[^<]*(</span>)',
        rf"\g<1>{solved}\g<2>",
        content,
    )

    INDEX_FILE.write_text(content, encoding="utf-8")


def main():
    info = get_info()
    rating = info.get("rating", 0)
    rank = info.get("rank", "unrated")
    solved = get_solved_count()

    update_html(rating, rank, solved)
    print(f"Codeforces synced: rating={rating} rank={rank} solved={solved}")


if __name__ == "__main__":
    main()
