#!/usr/bin/env python3
"""Check signing assets and the certificate chain embedded in a collection."""

import argparse
import base64
import json
import subprocess
import tempfile
from pathlib import Path


def openssl(*args, data=None):
    result = subprocess.run(
        ["openssl", *map(str, args)], input=data, capture_output=True, check=True
    )
    return result.stdout


def validate_assets(directory, minimum_days):
    directory = Path(directory)
    certificates = [directory / name for name in
                    ("signing-cert.cer", "intermediate.cer", "root.cer")]
    with tempfile.TemporaryDirectory() as temporary:
        pem = []
        for index, certificate in enumerate(certificates):
            path = Path(temporary) / f"certificate-{index}.pem"
            path.write_bytes(openssl("x509", "-inform", "DER", "-in", certificate))
            openssl("x509", "-in", path, "-checkend", minimum_days * 86400, "-noout")
            pem.append(path)
        usage = openssl("x509", "-in", pem[0], "-noout", "-ext", "extendedKeyUsage")
        if b"Code Signing" not in usage:
            raise ValueError("Signing certificate lacks Code Signing usage")
        leaf_public = openssl("x509", "-in", pem[0], "-pubkey", "-noout")
        leaf_public = openssl("pkey", "-pubin", "-outform", "DER", data=leaf_public)
        key_public = openssl("pkey", "-in", directory / "private-key.pem",
                             "-pubout", "-outform", "DER")
        if leaf_public != key_public:
            raise ValueError("Signing key does not match the certificate")
        openssl("verify", "-purpose", "any", "-CAfile", pem[2],
                "-untrusted", pem[1], pem[0])


def validate_embedded_chain(directory, collection):
    signed = json.loads(Path(collection).read_text())
    header = signed["signature"]["signature"].split(".")[0]
    header = json.loads(base64.urlsafe_b64decode(header + "=" * (-len(header) % 4)))
    embedded = [base64.b64decode(cert, validate=True) for cert in header["x5c"]]
    expected = [(Path(directory) / name).read_bytes() for name in
                ("signing-cert.cer", "intermediate.cer", "root.cer")]
    if embedded != expected:
        raise ValueError("Signed collection embeds a different certificate chain")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", help="Directory containing key and three DER certificates")
    parser.add_argument("--minimum-days", type=int, default=30)
    parser.add_argument("--collection", help="Also check the signed collection's embedded chain")
    args = parser.parse_args()
    if args.minimum_days < 0:
        parser.error("--minimum-days must be nonnegative")
    validate_assets(args.directory, args.minimum_days)
    if args.collection:
        validate_embedded_chain(args.directory, args.collection)
    print("Signing assets validated" + ("; embedded chain matches" if args.collection else ""))


if __name__ == "__main__":
    main()
