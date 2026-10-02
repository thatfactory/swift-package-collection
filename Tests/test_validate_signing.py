import base64
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "validate_signing", Path(__file__).resolve().parents[1] / "Scripts/validate_signing.py"
)
signing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(signing)


class SigningValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.directory = Path(cls.temporary.name)

        def run(*args):
            subprocess.run(["openssl", *map(str, args)], cwd=cls.directory,
                           check=True, capture_output=True)

        run("req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "365",
            "-subj", "/CN=Test Root", "-keyout", "root.key", "-out", "root.pem",
            "-addext", "basicConstraints=critical,CA:TRUE")
        for name, issuer, ca in [("intermediate", "root", True),
                                 ("signing-cert", "intermediate", False),
                                 ("no-usage", "intermediate", False)]:
            key = "private-key.pem" if name == "signing-cert" else name + ".key"
            run("req", "-new", "-newkey", "rsa:2048", "-nodes", "-subj", "/CN=" + name,
                "-keyout", key, "-out", name + ".csr")
            extensions = "basicConstraints=critical,CA:" + ("TRUE" if ca else "FALSE") + "\n"
            if name == "signing-cert":
                extensions += "extendedKeyUsage=critical,codeSigning\n"
            (cls.directory / "extensions.cnf").write_text(extensions)
            issuer_key = issuer + ".key"
            run("x509", "-req", "-in", name + ".csr", "-CA", issuer + ".pem",
                "-CAkey", issuer_key, "-CAcreateserial", "-days", "365",
                "-extfile", "extensions.cnf", "-out", name + ".pem")
        for name in ["root", "intermediate", "signing-cert", "no-usage"]:
            run("x509", "-in", name + ".pem", "-outform", "DER", "-out", name + ".cer")

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_valid_assets(self):
        signing.validate_assets(self.directory, 30)

    def test_insufficient_remaining_validity(self):
        with self.assertRaises(subprocess.CalledProcessError):
            signing.validate_assets(self.directory, 366)

    def test_wrong_key(self):
        key = self.directory / "private-key.pem"
        original = key.read_bytes()
        try:
            key.write_bytes((self.directory / "root.key").read_bytes())
            with self.assertRaisesRegex(ValueError, "does not match"):
                signing.validate_assets(self.directory, 30)
        finally:
            key.write_bytes(original)

    def test_missing_code_signing_usage(self):
        leaf = self.directory / "signing-cert.cer"
        original = leaf.read_bytes()
        try:
            leaf.write_bytes((self.directory / "no-usage.cer").read_bytes())
            with self.assertRaisesRegex(ValueError, "Code Signing"):
                signing.validate_assets(self.directory, 30)
        finally:
            leaf.write_bytes(original)

    def test_invalid_chain(self):
        intermediate = self.directory / "intermediate.cer"
        original = intermediate.read_bytes()
        try:
            intermediate.write_bytes((self.directory / "root.cer").read_bytes())
            with self.assertRaises(subprocess.CalledProcessError):
                signing.validate_assets(self.directory, 30)
        finally:
            intermediate.write_bytes(original)

    def test_embedded_chain_identity_and_order(self):
        chain = [base64.b64encode((self.directory / name).read_bytes()).decode()
                 for name in ["signing-cert.cer", "intermediate.cer", "root.cer"]]
        collection = self.directory / "collection.json"

        def write(chain):
            header = base64.urlsafe_b64encode(json.dumps({"x5c": chain}).encode()).decode().rstrip("=")
            collection.write_text(json.dumps({"signature": {"signature": header + ".payload.signature"}}))

        write(chain)
        signing.validate_embedded_chain(self.directory, collection)
        for invalid in [chain[::-1], chain[:1], [chain[1], *chain[1:]]]:
            write(invalid)
            with self.assertRaisesRegex(ValueError, "different certificate chain"):
                signing.validate_embedded_chain(self.directory, collection)


if __name__ == "__main__":
    unittest.main()
