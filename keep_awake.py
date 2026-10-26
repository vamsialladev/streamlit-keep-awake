"""Keep Streamlit Community Cloud apps awake.

Streamlit puts an app to sleep after about 12 hours without visitors. A plain
HTTP ping (curl) does not count as a visit, so this opens each app in a real
headless browser. If the app is asleep, it clicks the wake-up button and waits
for it to start. Run it on a schedule with GitHub Actions.

App URLs live in apps.txt next to this file.

Every visit adds `?source=keepawake`, so the hotel apps know it's this job: they load the page (which keeps the app
awake) but make no model call, write no log row and don't wake the database (hotel-ai-platform `bots`). Apps are
visited in parallel, at most KEEPAWAKE_PARALLEL (3) at a time, each in its own browser.
"""

import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import sync_playwright

APPS_FILE = Path(__file__).with_name("apps.txt")
SOURCE = "keepawake"
MAX_PARALLEL = int(os.getenv("KEEPAWAKE_PARALLEL", "3"))


def with_source(url: str) -> str:
    """The app URL with source=keepawake added (other query parameters kept)."""
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query) if k != "source"] + [("source", SOURCE)]
    return urlunsplit(parts._replace(query=urlencode(query)))


def load_apps(path: Path = APPS_FILE) -> list[str]:
    """Read app URLs from apps.txt: one per line, blank lines and # comments ignored."""
    apps = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            apps.append(line)
    return apps


WAKE_BUTTON = re.compile(r"get this app back up", re.IGNORECASE)


def visit(page, url: str) -> bool:
    """Open the app, wake it if asleep, and return True if it ends up awake."""
    page.goto(url, wait_until="domcontentloaded", timeout=90_000)
    page.wait_for_timeout(8_000)

    button = page.get_by_role("button", name=WAKE_BUTTON)
    if button.count() > 0:
        print(f"[asleep] {url} -> clicking wake-up button")
        button.first.click()
        page.wait_for_timeout(90_000)  # give the app time to boot
        page.reload(wait_until="domcontentloaded", timeout=90_000)
        page.wait_for_timeout(10_000)
    else:
        print(f"[awake]  {url}")
        page.wait_for_timeout(20_000)  # stay long enough to count as a visit

    name = url.split("//")[1].split(".")[0]
    page.screenshot(path=f"screenshot-{name}.png", full_page=True)

    still_asleep = page.get_by_role("button", name=WAKE_BUTTON).count() > 0
    if still_asleep:
        print(f"[FAILED] {url} is still asleep")
    return not still_asleep


def visit_in_own_browser(url: str) -> bool:
    """One app in its own browser (Playwright's sync API is per thread). Never raises: an error is a failure."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            try:
                return visit(page, with_source(url))
            finally:
                page.close()
                browser.close()
    except Exception as exc:  # keep going with the other apps
        print(f"[ERROR]  {url}: {exc}")
        return False


def run_all(apps: list[str], visit_one=visit_in_own_browser, parallel: int = MAX_PARALLEL) -> list[str]:
    """Visit every app, `parallel` at a time. Returns the apps that need attention."""
    with ThreadPoolExecutor(max_workers=max(1, parallel)) as pool:
        results = list(pool.map(visit_one, apps))
    return [url for url, ok in zip(apps, results, strict=True) if not ok]


def main() -> int:
    apps = load_apps()
    if not apps:
        print(f"No app URLs found in {APPS_FILE.name}")
        return 1

    failures = run_all(apps)
    if failures:
        print(f"\n{len(failures)} app(s) need attention: {failures}")
        return 1  # makes the workflow fail, so GitHub emails you
    print("\nAll apps awake.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
