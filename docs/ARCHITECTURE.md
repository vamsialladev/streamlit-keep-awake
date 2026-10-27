# Architecture

## System

```mermaid
flowchart LR
    CRON[GitHub Actions<br/>every 4 hours] --> KA[keep_awake.py]
    KA --> LIST[apps.txt]
    KA --> PW[Playwright<br/>headless Chromium]
    PW --> APPS[Streamlit Cloud apps<br/>the live stages]
    PW --> SHOT[screenshots<br/>workflow artifacts]
    KA -->|any app still asleep| FAIL[failed run<br/>email from GitHub]
    MONTH[monthly workflow] --> COMMIT[last-checked.txt commit<br/>keeps the schedule enabled]
    DAILY[daily workflow] --> SUM[failure summary<br/>hotel-ai-platform]
    SUM -->|errors over 5% or no successes| ISSUE[GitHub issue<br/>optional Slack]
```

## One visit

```mermaid
sequenceDiagram
    participant A as GitHub Actions
    participant K as keep_awake.py
    participant B as Chromium
    participant S as A Streamlit app
    A->>K: scheduled run
    K->>B: open the app URL with ?source=keepawake
    B->>S: load the page (a real session)
    alt asleep
        S-->>B: "Yes, get this app back up!"
        B->>S: click, wait 90 s, reload
    end
    B-->>K: screenshot, still asleep?
    K-->>A: exit 0, or 1 if any app is still asleep
```

## Components

| Component | Job |
|---|---|
| `keep_awake.py` | Reads `apps.txt`, opens up to `KEEPAWAKE_PARALLEL` apps at once (default 3), clicks the wake button if needed, saves a screenshot, exits 1 if any app stays asleep |
| `apps.txt` | The app URLs, one per line |
| `.github/workflows/keep-streamlit-awake.yml` | The 4-hourly schedule, screenshots kept 3 days |
| `.github/workflows/keepalive-commit.yml` | A monthly commit so GitHub doesn't disable the schedule after 60 days |
| `.github/workflows/daily-failure-summary.yml` | Runs hotel-ai-platform's daily summary over the shared request log and opens an issue when something needs attention |

## Scaling path

The visit list grows by one line per app. Past a dozen or so apps, split `apps.txt` across a job matrix. With real
traffic an app never sleeps, so in production always-on hosting replaces this repo; the health check in
hotel-ai-handoff stays.
