# Video script: streamlit-keep-awake (about 60 seconds)

I record this myself, in my own voice, over a screen recording of the repo on GitHub. Setup and tips:
`RECORDING_GUIDE.md` in my portfolio folder. Talk from the bullets, not word for word. `/` marks a natural pause.
Aim for 140–160 words a minute.

Before recording: sign in to GitHub, browser zoom 125%, open the repo's Actions tab.

## Shot list

| Time | On screen | What I say |
|---|---|---|
| 0–10 s | The README's first screen | My demos run on free Streamlit hosting, / and free apps go to sleep after about twelve hours. / So the first person I send a link to gets a "wake up" button and a thirty-second wait. |
| 10–25 s | `apps.txt`, then `keep_awake.py` | This fixes it. / Every four hours, a GitHub Action opens each app in a real headless browser. / If an app's asleep, it clicks the button and waits for it to start. |
| 25–40 s | Actions tab: open the latest "Keep Streamlit apps awake" run, then its screenshot artifact | Here's a run. / Every app gets a screenshot, so I can see it actually loaded. / If one stays asleep, the run fails and GitHub emails me. |
| 40–52 s | The README's Design at scale table | The visits are tagged, / so the apps don't count them as traffic or errors. / And there's a daily summary that opens an issue if an app's error rate goes over five percent. |
| 52–60 s | The repo page | It costs nothing, it calls no model, / and the code's on GitHub. |

## Exact inputs

Nothing to type. Open the most recent green run of the `Keep Streamlit apps awake` workflow and download its
`app-screenshots` artifact (kept 3 days, so record within 3 days of a run). Check the run before recording.

## LinkedIn caption (one sentence)

My free-hosted demos used to greet people with a "wake up" button, so a scheduled browser now visits each one every
four hours and tells me if one won't wake.
