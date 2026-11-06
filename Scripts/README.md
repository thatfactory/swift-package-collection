# Publication safeguards

Publication validates generated metadata on a temporary `collection-publish/` branch before advancing `main`. The required Review policy check must succeed on that exact signed commit; changes to `main`, the candidate identity, or files outside `packages.json` and `CHANGELOG.md` stop promotion. No policy-check bypass is used.

Failed or cancelled candidates may remain for diagnosis and can be removed after inspection. Infrastructure and agent-instruction changes run validation without publishing; use the existing manual Publish workflow after validating a publication-infrastructure change.

Run the safeguards without production credentials:

```sh
python3 -m unittest discover -s Tests -v
```
