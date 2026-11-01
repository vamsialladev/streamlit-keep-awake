# Security

## Reporting a vulnerability

Email <vamsialla.dev@gmail.com>. Please don't open a public issue.

## Threat model

| Asset | Threat | Mitigation |
|---|---|---|
| The repo's write token | The monthly workflow pushes a commit | `permissions: contents: write` only on that workflow; it only writes `last-checked.txt` |
| Supply chain | A compromised dependency or action | Pinned Python dependencies, pip-audit and gitleaks in CI, Dependabot for actions |
| The demos | Screenshots exposing data | The demos use synthetic data only; artifacts expire after 3 days |

## OWASP Top 10 for LLM applications

Not applicable: this repo calls no model. The apps it visits each have their own mapping in their SECURITY.md.
