# streamlit-keep-awake

Keeps my Streamlit Community Cloud apps from going to sleep, using a scheduled
GitHub Actions workflow.

## What it does

Every 4 hours, [`keep-streamlit-awake.yml`](.github/workflows/keep-streamlit-awake.yml)
runs [`keep_awake.py`](keep_awake.py), which opens each app listed in
[`apps.txt`](apps.txt) in a headless Chromium browser (Playwright):

- If the app is awake, it stays on the page long enough to count as a visit.
- If the app is asleep, it clicks the "get this app back up" button and waits
  for it to boot.
- It saves a screenshot of each app as a workflow artifact (kept 3 days).
- If any app is still asleep or errors out, the run fails, so GitHub emails you.

## Why a browser visit, not curl

Streamlit sleeps an app after about 12 hours without visitors. A plain HTTP
request (curl) only fetches the static shell page. It does not open the
websocket session that Streamlit counts as a visit, and it cannot click the
wake-up button. A real browser does both.

## Add an app

Add one URL per line to [`apps.txt`](apps.txt) and commit. Blank lines and
lines starting with `#` are ignored. No code changes needed.

## The 60-day inactivity rule

GitHub automatically disables scheduled workflows in a public repository when
there has been no repository activity for 60 days. To prevent that,
[`keepalive-commit.yml`](.github/workflows/keepalive-commit.yml) runs on the
1st of every month and commits an updated timestamp to `last-checked.txt`.

If the workflow gets disabled anyway:

1. Open the repo's **Actions** tab.
2. Select **Keep Streamlit apps awake** in the left sidebar.
3. Click **Enable workflow** in the banner.
4. Optionally click **Run workflow** to run it right away.

Or from the command line:

```sh
gh workflow enable keep-streamlit-awake.yml
gh workflow run keep-streamlit-awake.yml
```

Do the same for **Monthly keepalive commit** if it was disabled too.
