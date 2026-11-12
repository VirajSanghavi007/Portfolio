"""The Mac-style boot screen: shows once per tab session, fills its bar, can be skipped."""
import pytest

from conftest import visible_view

def state(page):
    """(reported %, bar width %, fading out?) or None once the boot screen is gone."""
    return page.evaluate("""() => { const b = document.getElementById('boot'); if (!b) return null;
      return [+b.getAttribute('aria-valuenow'), parseFloat(b.querySelector('.boot-bar i').style.width) || 0, b.classList.contains('out')]; }""")


@pytest.mark.parametrize("width,height", [(1242, 869), (390, 844)])
def test_first_visit_boots_then_shows_desktop(open_page, width, height):
    page = open_page(width=width, height=height, booted=False, fake_clock=True)
    box = page.locator("#boot").bounding_box()
    assert box == {"x": 0, "y": 0, "width": width, "height": height}
    assert page.is_visible("#boot .boot-logo")
    page.clock.run_for(3500)  # 2.3 s fill, a short hold, 0.5 s fade
    assert state(page) is None
    assert page.errors == []
    assert visible_view(page) == ["overview"]
    assert page.evaluate("sessionStorage.getItem('booted')") == "1"


STEPS = [(0, 0), (300, 6), (800, 24), (1100, 55), (1600, 62), (2000, 90), (2300, 100)]


def curve(t):
    """The fill the page should show t ms after it starts (same steps as index.html)."""
    t = max(0, t)
    for (ta, pa), (tb, pb) in zip(STEPS, STEPS[1:]):
        if t <= tb:
            return pa + (pb - pa) * (t - ta) / (tb - ta)
    return 100


def test_curve_helper():
    assert [curve(x) for x in (-5, 0, 150, 950, 1100, 5000)] == [0, 0, 3, 39.5, 55, 100]


def test_bar_fills_in_uneven_steps(open_page):
    page = open_page(booted=False, fake_clock=True)
    seen, t = [], 0
    # Times in ms since load: a slow start, a jump, a stall, a jump, then full. The page's own
    # clock starts a frame or two before ours, so each reading must fall in a short window.
    for at in [400, 900, 1200, 1500, 1900, 2300]:
        page.clock.run_for(at - t); t = at
        pct, width, out = state(page)
        assert curve(at - 20) - 1 <= pct <= curve(at + 60) + 1, (at, pct)
        assert abs(width - pct) <= 1, (at, width, pct)
        assert not out
        seen.append(pct)
    assert seen == sorted(seen)
    page.clock.run_for(150)
    assert state(page) == [100, 100, False]  # full, never past 100%, still showing
    page.clock.run_for(250)
    assert state(page)[2] is True  # fading out shortly after it fills
    page.clock.run_for(600)
    assert state(page) is None
    assert visible_view(page) == ["overview"]


def test_reload_in_same_tab_skips_boot(open_page):
    page = open_page(booted=False)
    page.wait_for_selector("#boot", state="detached", timeout=6000)
    page.reload()
    assert page.locator("#boot").count() == 0


def test_returning_tab_has_no_boot(page):
    assert page.locator("#boot").count() == 0


def test_query_forces_boot(open_page):
    page = open_page(hash_="?boot", fake_clock=True)  # a tab that has already booted
    assert page.is_visible("#boot")


def test_click_skips(open_page):
    page = open_page(booted=False, fake_clock=True)
    page.clock.run_for(300)
    page.click("#boot")
    skipped = state(page)
    assert skipped[2] is True
    page.clock.run_for(200)
    assert state(page) == skipped  # the bar stops moving once skipped
    page.clock.run_for(400)
    assert state(page) is None
    assert page.evaluate("sessionStorage.getItem('booted')") == "1"
    page.click('.side .nav button[data-view="about"]')
    assert visible_view(page) == ["about"]


def test_key_skips_without_triggering_shortcuts(open_page):
    page = open_page(booted=False, fake_clock=True)
    page.keyboard.press("Control+k")
    page.clock.run_for(600)
    assert state(page) is None
    assert page.is_hidden("#palette")
    page.keyboard.press("Control+k")  # after boot, shortcuts work again
    assert page.is_visible("#palette")


def test_skipping_twice_is_harmless(open_page):
    page = open_page(booted=False, fake_clock=True)
    page.click("#boot")
    page.clock.run_for(300)
    page.evaluate("document.getElementById('boot').click()")
    page.clock.run_for(600)
    assert state(page) is None
    assert page.errors == []


def test_reduced_motion_skips_boot(open_page):
    page = open_page(booted=False, reduced_motion="reduce")
    assert page.locator("#boot").count() == 0


def test_blocked_storage_skips_boot(open_page):
    page = open_page(booted=False, init_script="Object.defineProperty(window, 'sessionStorage', { get() { throw new Error('blocked'); } });")
    assert page.locator("#boot").count() == 0
    assert page.errors == []
