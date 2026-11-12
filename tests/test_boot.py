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
    page.clock.run_for(6000)  # up to 5 s fill, a short hold, 0.5 s fade
    assert state(page) is None
    assert page.errors == []
    assert visible_view(page) == ["overview"]
    assert page.evaluate("sessionStorage.getItem('booted')") == "1"


SHAPE = [(0, 0), (0.13, 6), (0.35, 24), (0.48, 55), (0.7, 62), (0.87, 90), (1, 100)]  # (share of the fill time, %)


def curve(t, fill):
    """The fill the page should show t ms after it starts, for a fill lasting `fill` ms (same steps as index.html)."""
    t = max(0, t)
    steps = [(f * fill, pct) for f, pct in SHAPE]
    for (ta, pa), (tb, pb) in zip(steps, steps[1:]):
        if t <= tb:
            return pa + (pb - pa) * (t - ta) / (tb - ta)
    return 100


def test_curve_helper():
    assert [curve(x, 1000) for x in (-5, 0, 65, 415, 480, 9000)] == [0, 0, 3, 39.5, 55, 100]
    assert curve(1770, 3000) == pytest.approx(58.5)


def pin_random(r):
    """Init script making Math.random() always return r, so the page picks a known fill time."""
    return f"Math.random = () => {r};"


# Math.random() -> fill time: 3 s at the bottom of its range, 5 s at the top.
@pytest.mark.parametrize("r,fill", [(0, 3000), (0.5, 4000), (0.99995, 4999.9)])
def test_bar_fills_in_uneven_steps_over_3_to_5_seconds(open_page, r, fill):
    page = open_page(booted=False, fake_clock=True, init_script=pin_random(r))
    seen, t = [], 0
    # A slow start, a jump, a stall, a jump, then full. The page's own clock starts a frame
    # or two before ours, so each reading must fall in a short window.
    for at in [round(f * fill) for f in (0.17, 0.39, 0.52, 0.65, 0.83, 0.95)] + [round(fill) - 100]:
        page.clock.run_for(at - t); t = at
        pct, width, out = state(page)
        assert curve(at - 20, fill) - 1 <= pct <= curve(at + 60, fill) + 1, (at, pct)
        assert abs(width - pct) <= 1, (at, width, pct)
        assert not out
        seen.append(pct)
    assert seen == sorted(seen)
    assert seen[-1] < 100  # not full until the end of the fill time
    page.clock.run_for(round(fill) + 150 - t)
    assert state(page) == [100, 100, False]  # full, never past 100%, still showing
    page.clock.run_for(250)
    assert state(page)[2] is True  # fading out shortly after it fills
    page.clock.run_for(600)
    assert state(page) is None
    assert visible_view(page) == ["overview"]


def test_star_spins_while_loading(open_page):
    page = open_page(booted=False, fake_clock=True)  # the fill waits for the fake clock; CSS animations run in real time
    spin = page.evaluate("""() => { const a = document.querySelector('#boot .boot-logo').getAnimations()[0];
      const t = a.effect.getTiming(); return [a.animationName, t.duration, t.iterations, a.effect.getKeyframes().at(-1).transform]; }""")
    assert spin == ["boot-spin", 2400, float("inf"), "rotate(360deg)"]  # spins forever
    angle = """() => { const [a, b] = getComputedStyle(document.querySelector('#boot .boot-logo')).transform.slice(7, -1).split(',').map(Number);
      return Math.atan2(b, a) * 180 / Math.PI; }"""
    first = page.evaluate(angle)
    page.wait_for_function(f"a => Math.abs(({angle})() - a) > 5", arg=first, timeout=3000)  # it is actually turning


def test_reload_in_same_tab_skips_boot(open_page):
    page = open_page(booted=False)
    page.wait_for_selector("#boot", state="detached", timeout=10000)
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
