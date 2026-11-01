# Decisions

## 1. A real browser, not a ping

- **Context:** Streamlit counts a websocket session as a visit; a sleeping app needs a button click.
- **Decision:** Playwright with headless Chromium.
- **Tradeoff:** about a minute of Actions time per app per run instead of a second.
- **Result:** apps wake and stay awake; a run fails when one doesn't.

## 2. No Dockerfile

- **Context:** the portfolio standard asks every repo for a Dockerfile.
- **Decision:** none here: the job only runs in GitHub Actions, which already provides the runner image.
- **Tradeoff:** to run it elsewhere, install Python and Playwright (README, Run locally).
- **Result:** one less image to keep patched.
