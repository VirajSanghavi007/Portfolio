"""The headshot on the About page: a small square file, shown round beside the heading."""
import pathlib

import pytest
from PIL import Image

PHOTO = pathlib.Path(__file__).resolve().parent.parent / "Images" / "viraj.webp"


def test_photo_file_is_small_and_square():
    with Image.open(PHOTO) as im:
        assert im.format == "WEBP"
        assert im.size == (480, 480)
    assert PHOTO.stat().st_size < 60_000


@pytest.mark.parametrize("width,height", [(1242, 869), (390, 844)])
def test_about_shows_round_photo_beside_heading(open_page, width, height):
    page = open_page(width=width, height=height, hash_="#about")
    img = page.locator('.view[data-for="about"] .me img')
    assert img.get_attribute("alt") == "Viraj Sanghavi"
    img.wait_for(state="visible")
    assert page.evaluate("() => { const i = document.querySelector('.me img'); return i.complete && i.naturalWidth; }") == 480
    box, h1 = img.bounding_box(), page.locator(".me h1.page").bounding_box()
    assert box["width"] == box["height"] == 88
    assert h1["x"] - (box["x"] + box["width"]) == 18  # photo sits 18 px left of the heading
    text = page.evaluate("""() => { const r = document.createRange(); r.selectNodeContents(document.querySelector('.me h1.page'));
      const b = r.getBoundingClientRect(); return [b.top, b.height]; }""")  # the text itself, not the h1 box
    assert abs((box["y"] + 44) - (text[0] + text[1] / 2)) < 1  # vertically centred on the photo
    assert page.evaluate("getComputedStyle(document.querySelector('.me img')).borderTopWidth") == "1px"
    assert page.evaluate("getComputedStyle(document.querySelector('.me img')).borderRadius") == "50%"
    assert page.evaluate("getComputedStyle(document.querySelector('.me img')).objectFit") == "cover"
    below_crumbs = """sel => document.querySelector(sel).getBoundingClientRect().top - document.querySelector('.crumbs').getBoundingClientRect().bottom"""
    me_top = page.evaluate(below_crumbs, ".me")
    gap_below = page.evaluate("""() => document.querySelector('.view[data-for="about"] p').getBoundingClientRect().top - document.querySelector('.me').getBoundingClientRect().bottom""")
    page.click('.side .nav button[data-view="work"]') if width > 760 else page.evaluate("location.hash = 'work'")
    assert me_top == page.evaluate(below_crumbs, '.view[data-for="work"] h1.page')  # lines up with the other page headings
    assert gap_below == 14
    assert page.errors == []
