"""
Daily sync: pulls current solved-count by difficulty from LeetCode's public
GraphQL endpoint and updates the numbers already present in the #dsa-practice
section of index.html.

LeetCode has no official REST API, but the GraphQL endpoint used by the site
itself (leetcode.com/graphql) returns public profile stats with no auth needed
for a public username.
"""
import json
import re
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = REPO_ROOT / "index.html"
USERNAME = "Viraj_Sanghavi"

QUERY = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile { ranking }
    submitStatsGlobal { acSubmissionNum { difficulty count } }
  }
  allQuestionsCount { difficulty count }
}
"""


def fetch_stats():
    payload = json.dumps({"query": QUERY, "variables": {"username": USERNAME}}).encode("utf-8")
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            "Referer": f"https://leetcode.com/{USERNAME}/",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    data = fetch_stats()
    solved = {e["difficulty"]: e["count"] for e in data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]}
    total_q = {e["difficulty"]: e["count"] for e in data["data"]["allQuestionsCount"]}

    total = solved.get("All", 0)
    easy, easy_total = solved.get("Easy", 0), total_q.get("Easy", 0)
    medium, medium_total = solved.get("Medium", 0), total_q.get("Medium", 0)
    hard, hard_total = solved.get("Hard", 0), total_q.get("Hard", 0)
    ranking = data["data"]["matchedUser"]["profile"]["ranking"]

    content = INDEX_FILE.read_text(encoding="utf-8")
    content = re.sub(r'(id="lcTotal" data-target=")\d+(")', rf"\g<1>{total}\g<2>", content)
    content = re.sub(r'(id="lcEasy">)[^<]*(</span>)', rf"\g<1>{easy} / {easy_total}\g<2>", content)
    content = re.sub(r'(id="lcMedium">)[^<]*(</span>)', rf"\g<1>{medium} / {medium_total}\g<2>", content)
    content = re.sub(r'(id="lcHard">)[^<]*(</span>)', rf"\g<1>{hard} / {hard_total}\g<2>", content)
    content = re.sub(r'(id="lcRanking">)[^<]*(</span>)', rf"\g<1>#{ranking:,}\g<2>", content)
    INDEX_FILE.write_text(content, encoding="utf-8")

    print(f"LeetCode synced: total={total} easy={easy}/{easy_total} medium={medium}/{medium_total} hard={hard}/{hard_total} ranking=#{ranking}")


if __name__ == "__main__":
    main()
