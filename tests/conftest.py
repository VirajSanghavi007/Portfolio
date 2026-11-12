"""Shared fixtures: one real Chrome per test module, a fresh browser context (clean state) per test."""
import pathlib

import pytest
from playwright.sync_api import sync_playwright

INDEX = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()


@pytest.fixture(scope="module")
def browser():
    """System Chrome via Playwright. Skips (not fails) when Chrome cannot start."""
    pw = sync_playwright().start()
    try:
        b = pw.chromium.launch(channel="chrome")
    except Exception as e:  # Chrome missing or blocked
        pw.stop()
        pytest.skip(f"chrome_available: no system Chrome ({e})")
    yield b
    b.close()
    pw.stop()


def _open(browser, width=1242, height=869, init_script=None, fixed_time=None, hash_=""):
    ctx = browser.new_context(viewport={"width": width, "height": height})
    if init_script:
        ctx.add_init_script(init_script)
    page = ctx.new_page()
    page.errors = []
    page.on("console", lambda m: page.errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: page.errors.append(str(e)))
    if fixed_time:
        page.clock.set_fixed_time(fixed_time)
    page.goto(INDEX + hash_)
    return page


@pytest.fixture
def open_page(browser):
    """Factory: open_page(width=..., init_script=..., fixed_time=..., hash_=...) -> page in a new context."""
    pages = []

    def make(**kw):
        p = _open(browser, **kw)
        pages.append(p)
        return p

    yield make
    for p in pages:
        p.context.close()


@pytest.fixture
def page(open_page):
    return open_page()


def visible_view(page):
    return page.eval_on_selector_all(".view", "vs => vs.filter(v => !v.hidden).map(v => v.dataset.for)")
