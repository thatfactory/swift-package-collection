# Collection signing

The Publish workflow generates, signs, and deploys the collection to GitHub Pages.
Signing assets are stored as base64-encoded GitHub Actions secrets:

| Secret | Decoded format |
| --- | --- |
| `PACKAGE_COLLECTION_SIGNING_KEY` | Unencrypted PEM private key |
| `PACKAGE_COLLECTION_SIGNING_CERT` | DER leaf certificate |
| `PACKAGE_COLLECTION_CA_INTERMEDIATE` | DER intermediate certificate |
| `PACKAGE_COLLECTION_CA_ROOT` | DER root certificate |

Keep private keys outside the repository, in a restricted directory. Never put
keys, encoded secret values, or account details in commits, issues, or logs.

## Annual renewal

Renew before the leaf certificate expires. The current publishing validation
requires at least 30 days of remaining validity for every certificate in the chain.

1. Confirm the intended team in Apple Developer Certificates, Identifiers & Profiles.
2. Create a fresh key and certificate signing request (CSR). Upload only the CSR
   to Apple; retain the private key locally.
3. Select **Swift Package Collection Certificate** when available. Apple also
   offers **Swift Package Certificate** for SwiftPM 5.9 or later; changing types
   requires checking compatibility with the signer and supported consumers.
4. Download the new leaf certificate and inspect its issuer, validity, and Code
   Signing usage. Obtain its actual intermediate and root from
   [Apple PKI](https://www.apple.com/certificateauthority/). Do not assume that a
   replacement uses the same issuer as its predecessor.
5. In a restricted directory, name the files `private-key.pem`, `signing-cert.cer`,
   `intermediate.cer`, and `root.cer`. Run:

   ```sh
   python3 Scripts/validate_signing.py /path/to/signing-assets
   ```

6. Sign a copy of the current collection with the workflow's pinned generator
   branch and full chain in leaf → intermediate → root order. Check the embedded
   chain with `--collection /path/to/collection.signed.json`, then consume the
   signed file with `swift package-collection add file:///path/to/collection.signed.json`.
   Keep signature verification enabled and remove the temporary source afterward.
7. Ensure no Publish job is active while rotating secrets. Set all four secrets
   from the validated files using a secure local process; base64 is encoding,
   not encryption. Never print the values.
8. Dispatch **Publish** on `main` with `force_publish=true` to publish the renewed
   signature even when package metadata is unchanged. This bumps the catalog revision.
9. Require a successful deployment. Fetch the live collection and compare its
   embedded leaf fingerprint, expiration, and full chain with the replacement.
   Add or refresh the production URL in SwiftPM with normal signature verification.

The embedded-chain check verifies certificate identity; the signer and SwiftPM
verify the collection signature. Neither check substitutes for the other.

## Recovery

Keep the previous working assets securely until production verification succeeds.
Routine renewal does not require revoking the old certificate. If signing or
deployment fails, inspect the failing job before dispatching another run. Restore
all four previous secrets together only if that identity remains valid and has
not been revoked; then force-publish and verify the live collection again.

For expiry, revocation, or a compromised key, issue a fresh certificate rather
than bypassing signature checks. Update this procedure if the certificate type
or chain changes. Do not publish an unsigned collection as a renewal workaround.
