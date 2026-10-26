"""keep_awake.py without a browser: the app list and the per-app decision (a fake page stands in for Playwright)."""

import keep_awake


class FakeButton:
    def __init__(self, page):
        self.page = page

    def count(self):
        return 1 if self.page.asleep else 0

    @property
    def first(self):
        return self

    def click(self):
        self.page.clicks += 1
        self.page.asleep = self.page.stays_asleep


class FakePage:
    def __init__(self, asleep=False, stays_asleep=False):
        self.asleep, self.stays_asleep, self.clicks, self.shots, self.visited = asleep, stays_asleep, 0, [], []

    def goto(self, url, **_):
        self.visited.append(url)

    def wait_for_timeout(self, _ms):
        pass

    def reload(self, **_):
        pass

    def get_by_role(self, role, name):
        assert role == "button" and name.search("Yes, get this app back up!")
        return FakeButton(self)

    def screenshot(self, path, **_):
        self.shots.append(path)


def test_load_apps_skips_blank_lines_and_comments(tmp_path):
    f = tmp_path / "apps.txt"
    f.write_text("# header\n\nhttps://a.streamlit.app  # inline note\n   \nhttps://b.streamlit.app\n", encoding="utf-8")
    assert keep_awake.load_apps(f) == ["https://a.streamlit.app", "https://b.streamlit.app"]


def test_the_checked_in_list_is_valid():
    apps = keep_awake.load_apps()
    assert apps and all(a.startswith("https://") and a.endswith(".streamlit.app") for a in apps)
    assert len(apps) == len(set(apps))


def test_an_awake_app_is_visited_and_screenshotted():
    page = FakePage()
    assert keep_awake.visit(page, "https://hotel-ops-assistant.streamlit.app") is True
    assert page.clicks == 0 and page.shots == ["screenshot-hotel-ops-assistant.png"]


def test_a_sleeping_app_gets_the_wake_button_clicked():
    page = FakePage(asleep=True)
    assert keep_awake.visit(page, "https://eval-harness.streamlit.app") is True and page.clicks == 1


def test_an_app_that_stays_asleep_fails_the_run():
    page = FakePage(asleep=True, stays_asleep=True)
    assert keep_awake.visit(page, "https://guest-request-agent.streamlit.app") is False


def test_every_visit_says_it_is_the_keep_awake_job():
    assert keep_awake.with_source("https://a.streamlit.app") == "https://a.streamlit.app?source=keepawake"
    assert (
        keep_awake.with_source("https://a.streamlit.app/?v=1&source=x")
        == "https://a.streamlit.app/?v=1&source=keepawake"
    )


def test_apps_run_in_parallel_and_failures_are_reported():
    import threading
    import time

    running, peak, lock = [0], [0], threading.Lock()

    def fake_visit(url):
        with lock:
            running[0] += 1
            peak[0] = max(peak[0], running[0])
        time.sleep(0.05)
        with lock:
            running[0] -= 1
        return "bad" not in url

    apps = [f"https://app{i}.streamlit.app" for i in range(6)] + ["https://bad.streamlit.app"]
    assert keep_awake.run_all(apps, fake_visit, parallel=3) == ["https://bad.streamlit.app"]
    assert peak[0] == 3  # never more than three browsers at once
