"""Promote a generated metadata commit only after its real policy CI succeeds."""

import argparse
import json
import os
import re
import subprocess
import time


REPOSITORY = "thatfactory/swift-package-collection"
WORKFLOW = ".github/workflows/review-policy.yml"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def validate_commit(commit, base, candidate):
    require(commit["sha"] == candidate, "Unexpected candidate commit.")
    require([p["sha"] for p in commit["parents"]] == [base], "Candidate base changed.")
    require(commit["commit"]["verification"]["verified"], "Candidate signature is unverified.")
    files = commit["files"]
    require(bool(files), "Candidate contains no metadata changes.")
    require(all(f["filename"] in {"packages.json", "CHANGELOG.md"}
                and f["status"] == "modified" and "previous_filename" not in f
                for f in files), "Candidate changes more than generated metadata.")


def policy_state(runs, checks, branch, candidate, workflow_id):
    require(runs["total_count"] <= 100, "Policy run pagination is incomplete.")
    require(checks["total_count"] <= 100, "Policy check pagination is incomplete.")
    matching = [r for r in runs["workflow_runs"]
                if r["head_sha"] == candidate and r["head_branch"] == branch
                and r["event"] == "push" and r["workflow_id"] == workflow_id
                and r["repository"]["full_name"] == REPOSITORY]
    if not matching:
        return "pending"
    latest = max(matching, key=lambda r: (r["id"], r["run_attempt"]))
    if latest["status"] != "completed":
        return "pending"
    require(latest["conclusion"] == "success", "Candidate policy workflow failed.")
    matching_checks = [c for c in checks["check_runs"]
                       if c["name"] == "Review policy" and c["head_sha"] == candidate
                       and c["app"]["id"] == 15368
                       and c["check_suite"]["id"] == latest["check_suite_id"]]
    if not matching_checks:
        return "pending"
    check = max(matching_checks, key=lambda c: c["id"])
    if check["status"] != "completed":
        return "pending"
    require(check["conclusion"] == "success", "Candidate policy check failed.")
    return "success"


class GitHub:
    def request(self, path, method="GET", body=None, write=False):
        env = os.environ.copy()
        if write:
            env["GH_TOKEN"] = env["PUBLISH_TOKEN"]
        command = ["gh", "api", "--method", method, f"repos/{REPOSITORY}/{path}"]
        if body is not None:
            command += ["--input", "-"]
        result = subprocess.run(command, input=json.dumps(body) if body is not None else None,
                                text=True, capture_output=True, env=env)
        require(result.returncode == 0, f"GitHub {method} {path} failed; no promotion authorized.")
        return json.loads(result.stdout) if result.stdout.strip() else None


def validate_refs(api, branch, base, candidate):
    require(api.request(f"git/ref/heads/{branch}")["object"]["sha"] == candidate,
            "Candidate branch changed.")
    require(api.request("git/ref/heads/main")["object"]["sha"] == base,
            "Main changed; regenerate the publication candidate.")


def promote(api, branch, base, candidate, timeout=600, clock=time.monotonic, sleep=time.sleep):
    require(re.fullmatch(r"collection-publish/\d+-\d+", branch), "Invalid candidate branch.")
    require(all(re.fullmatch(r"[0-9a-f]{40}", sha) for sha in (base, candidate)), "Invalid commit identity.")
    validate_refs(api, branch, base, candidate)
    validate_commit(api.request(f"commits/{candidate}"), base, candidate)
    workflow = api.request("actions/workflows/review-policy.yml")
    require(workflow["path"] == WORKFLOW and isinstance(workflow["id"], int),
            "Unexpected policy workflow identity.")
    deadline = clock() + timeout
    while True:
        runs = api.request(f"actions/workflows/review-policy.yml/runs?head_sha={candidate}&per_page=100")
        checks = api.request(f"commits/{candidate}/check-runs?per_page=100")
        if policy_state(runs, checks, branch, candidate, workflow["id"]) == "success":
            break
        require(clock() < deadline, "Candidate policy check timed out; main was not advanced.")
        sleep(15)
    validate_refs(api, branch, base, candidate)
    result = api.request("git/refs/heads/main", "PATCH", {"sha": candidate, "force": False}, write=True)
    require(result["object"]["sha"] == candidate, "Main promotion returned an unexpected commit.")
    # Never delete a branch that another actor changed while publication ran.
    if api.request(f"git/ref/heads/{branch}")["object"]["sha"] == candidate:
        api.request(f"git/refs/heads/{branch}", "DELETE", write=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--candidate", required=True)
    args = parser.parse_args()
    try:
        promote(GitHub(), args.branch, args.base, args.candidate)
    except (KeyError, RuntimeError, ValueError) as error:
        raise SystemExit(str(error))
    print(f"Promoted validated collection metadata {args.candidate}.")
