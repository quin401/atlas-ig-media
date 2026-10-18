"""Push local media files to quin401/atlas-ig-media via the GitHub Contents API.
Usage: python3 push_media.py <repo_dir_prefix> <file> [<file> ...]
Prints the public raw URL for each file. Token is read from ./.gh_token (never printed)."""
import base64, json, os, sys, urllib.request, urllib.error
REPO = "quin401/atlas-ig-media"
TOKEN = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gh_token")).read().strip()

def api(method, path, body=None):
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/contents/{path}", method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise SystemExit(f"GitHub {e.code}: {e.read().decode()[:300]}")

prefix, files = sys.argv[1].strip("/"), sys.argv[2:]
for f in files:
    path = f"{prefix}/{os.path.basename(f)}"
    existing = api("GET", path)
    body = {"message": f"Add {path}", "content": base64.b64encode(open(f, "rb").read()).decode()}
    if existing and "sha" in existing:
        body["sha"] = existing["sha"]
        body["message"] = f"Update {path}"
    api("PUT", path, body)
    print(f"https://raw.githubusercontent.com/{REPO}/main/{path}")
