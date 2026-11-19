# -*- coding: utf-8 -*-
"""Create/configure the GitHub Pages repo using the local git credential helper."""
import json
import subprocess
import sys
import urllib.error
import urllib.request

REPO = "mrlabhk.com"
DOMAIN = "www.mrlabhk.com"


def get_credential():
    p = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git credential fill failed: " + p.stderr.strip())
    out = {}
    for line in p.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k] = v
    if not out.get("username") or not out.get("password"):
        raise RuntimeError("no GitHub credential available")
    return out["username"], out["password"]


def api(method, path, token, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request("https://api.github.com" + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "mrlabhk-deploy")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
            return r.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"raw": raw.decode("utf-8", "replace")[:500]}
        return e.code, parsed


def main():
    user, token = get_credential()
    status, me = api("GET", "/user", token)
    if status != 200:
        raise SystemExit("GET /user failed: " + str(status) + " " + str(me))
    login = me["login"]
    print("authenticated_as=" + login)

    status, repo = api("GET", "/repos/" + login + "/" + REPO, token)
    if status == 404:
        status, repo = api("POST", "/user/repos", token, {
            "name": REPO,
            "description": "MR Lab 化驗所優惠站 - 香港體檢計劃比較",
            "homepage": "https://" + DOMAIN,
            "public": True,
            "has_issues": False,
            "has_wiki": False,
            "has_projects": False
        })
    if status not in (200, 201):
        raise SystemExit("create repo failed: " + str(status) + " " + str(repo))
    print("repo=" + repo["full_name"])
    print("clone_url=" + repo["clone_url"])
    print("html_url=" + repo["html_url"])

    # Configure GitHub Pages (branch main, root folder).
    status, pages = api("POST", "/repos/" + login + "/" + REPO + "/pages", token, {
        "build_type": "legacy",
        "source": {"branch": "main", "path": "/"}
    })
    print("pages_put=" + str(status))
    if status >= 400:
        print("pages_put_error=" + json.dumps(pages, ensure_ascii=False)[:600])

    # Custom domain + enforce HTTPS.
    status, upd = api("PATCH", "/repos/" + login + "/" + REPO + "/pages", token, {
        "cname": DOMAIN,
        "https_enforced": True,
        "public": True
    })
    print("pages_patch=" + str(status))
    if status >= 400:
        print("pages_patch_error=" + json.dumps(upd, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main()
