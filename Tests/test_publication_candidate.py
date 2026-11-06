import copy
import importlib.util
from pathlib import Path
import unittest


spec = importlib.util.spec_from_file_location(
    "publication", Path(__file__).resolve().parents[1] / "Scripts/promote_collection_candidate.py")
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)

BASE = "a" * 40
CANDIDATE = "b" * 40
BRANCH = "collection-publish/123-1"


class FakeGitHub:
    def __init__(self):
        self.main_reads = 0
        self.branch_reads = 0
        self.change_main = False
        self.change_branch = False
        self.unavailable = False
        self.writes = []
        self.commit = {"sha": CANDIDATE, "parents": [{"sha": BASE}],
                       "commit": {"verification": {"verified": True}},
                       "files": [{"filename": "packages.json", "status": "modified"},
                                 {"filename": "CHANGELOG.md", "status": "modified"}]}
        self.runs = {"total_count": 1, "workflow_runs": [
            {"id": 1, "run_attempt": 1, "head_sha": CANDIDATE, "head_branch": BRANCH,
             "event": "push", "path": publication.WORKFLOW, "workflow_id": 7, "status": "completed",
             "conclusion": "success", "check_suite_id": 42,
             "repository": {"full_name": publication.REPOSITORY}}]}
        self.checks = {"total_count": 1, "check_runs": [
            {"id": 1, "name": "Review policy", "head_sha": CANDIDATE,
             "app": {"id": 15368}, "check_suite": {"id": 42},
             "status": "completed", "conclusion": "success"}]}

    def request(self, path, method="GET", body=None, write=False):
        if self.unavailable:
            raise RuntimeError("Unavailable policy evidence")
        if write:
            self.writes.append((path, method, body))
            return {"object": {"sha": CANDIDATE}} if method == "PATCH" else None
        if path == "git/ref/heads/main":
            self.main_reads += 1
            return {"object": {"sha": "c" * 40 if self.change_main and self.main_reads > 1 else BASE}}
        if path == f"git/ref/heads/{BRANCH}":
            self.branch_reads += 1
            return {"object": {"sha": "c" * 40 if self.change_branch and self.branch_reads > 1 else CANDIDATE}}
        if path == f"commits/{CANDIDATE}":
            return self.commit
        if path == "actions/workflows/review-policy.yml":
            return {"id": 7, "path": publication.WORKFLOW}
        if path.startswith("actions/workflows/"):
            return self.runs
        if "/check-runs?" in path:
            return self.checks
        raise AssertionError(path)


class PublicationCandidateTests(unittest.TestCase):
    def promote(self, api):
        # No live API, signing credentials, or real sleeps in these boundary tests.
        publication.promote(api, BRANCH, BASE, CANDIDATE, timeout=0, sleep=lambda _: None)

    def rejects(self, api):
        with self.assertRaises(RuntimeError):
            self.promote(api)
        self.assertEqual(api.writes, [])

    def test_validated_metadata_uses_fast_forward_and_cleans_owned_branch(self):
        api = FakeGitHub()
        self.promote(api)
        self.assertEqual(api.writes, [
            ("git/refs/heads/main", "PATCH", {"sha": CANDIDATE, "force": False}),
            (f"git/refs/heads/{BRANCH}", "DELETE", None)])

    def test_changed_publication_identities_are_rejected(self):
        for key in ("change_main", "change_branch"):
            with self.subTest(key=key):
                api = FakeGitHub()
                setattr(api, key, True)
                self.rejects(api)

    def test_unreviewed_files_or_parents_cannot_be_promoted(self):
        mutations = [
            lambda c: c["files"].append({"filename": "AGENTS.md", "status": "modified"}),
            lambda c: c["parents"].append({"sha": "c" * 40}),
            lambda c: c["parents"][0].update(sha="c" * 40),
            lambda c: c["commit"]["verification"].update(verified=False),
            lambda c: c["files"][0].update(status="renamed", previous_filename="AGENTS.md"),
        ]
        for mutate in mutations:
            api = FakeGitHub()
            mutate(api.commit)
            self.rejects(api)

    def test_missing_failed_and_stale_policy_results_fail_closed(self):
        mutations = [
            lambda a: a.checks["check_runs"].clear(),
            lambda a: a.runs["workflow_runs"].clear(),
            lambda a: a.runs["workflow_runs"][0].update(head_sha=BASE),
            lambda a: a.runs["workflow_runs"][0].update(head_branch="other"),
            lambda a: a.runs["workflow_runs"][0].update(workflow_id=8),
            lambda a: a.runs["workflow_runs"][0].update(conclusion="failure"),
            lambda a: a.checks["check_runs"][0].update(head_sha=BASE),
            lambda a: a.checks["check_runs"][0]["app"].update(id=1),
            lambda a: a.checks["check_runs"][0]["check_suite"].update(id=43),
            lambda a: a.checks["check_runs"][0].update(conclusion="failure"),
            lambda a: a.checks.update(total_count=101),
            lambda a: a.runs.update(total_count=101),
        ]
        for mutate in mutations:
            api = FakeGitHub()
            mutate(api)
            self.rejects(api)

    def test_failed_rerun_overrides_previous_success(self):
        api = FakeGitHub()
        failed = copy.deepcopy(api.runs["workflow_runs"][0])
        failed.update(run_attempt=2, conclusion="failure")
        api.runs["workflow_runs"].append(failed)
        self.rejects(api)

    def test_ref_qualified_workflow_path_uses_verified_workflow_id(self):
        for suffix in ("", "@main", "@" + BRANCH, "@refs/heads/" + BRANCH):
            with self.subTest(suffix=suffix):
                api = FakeGitHub()
                api.runs["workflow_runs"][0]["path"] += suffix
                self.promote(api)
                self.assertEqual(api.writes[0][2]["sha"], CANDIDATE)

    def test_unavailable_policy_evidence_cannot_promote(self):
        api = FakeGitHub()
        api.unavailable = True
        self.rejects(api)
