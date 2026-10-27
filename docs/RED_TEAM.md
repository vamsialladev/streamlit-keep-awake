# Red team

There's no model and no user input here, so there's nothing to prompt-inject. The red-team results for the apps it
visits are in each app's own `docs/RED_TEAM.md`, and the shared corpus is in
[hotel-ai-platform](https://github.com/vamsialladev/hotel-ai-platform/blob/main/docs/RED_TEAM.md).

What could go wrong in this repo, and what stops it today:

| Risk | What stops it | Gap |
|---|---|---|
| Someone changes `apps.txt` so the job visits a site I don't own | Changes reach `main` only through my review (CODEOWNERS) | `keep_awake.py` doesn't check that a URL is a `streamlit.app` address |
| A pull request from a fork reads the `OPS_DATABASE_URL` or Slack secret | GitHub doesn't pass secrets to workflows run for fork pull requests; the summary job runs only on its schedule | none known |
| A workflow token does more than it needs | `ci.yml` and the visit job read only; the summary job can also open issues; only the monthly keepalive commit can write | none known |
| The daily summary posts personal data | It reads the shared request log, which is redacted before it's written (hotel-ai-platform) | none known |

A `streamlit.app`-only check on `apps.txt` is a small fix; it's on the roadmap, not done.
