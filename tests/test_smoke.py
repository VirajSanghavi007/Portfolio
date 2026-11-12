"""Smoke: the page opens cleanly at desktop and phone width."""
import pytest

from conftest import visible_view


@pytest.mark.parametrize("width,height", [(1242, 869), (390, 844)])
def test_loads_without_errors_or_sideways_scroll(open_page, width, height):
    page = open_page(width=width, height=height)
    page.wait_for_timeout(300)
    assert page.errors == []
    assert page.title() == "Viraj Sanghavi | AI/ML Engineer"
    assert page.evaluate("document.documentElement.scrollWidth") <= width
    assert visible_view(page) == ["overview"]
    assert page.is_hidden("#palette")
    assert page.is_visible("text=I haven't tried to break.")
    dock = page.locator(".dock").bounding_box()  # fixed, so scrollWidth cannot see it
    assert dock["x"] >= 0 and dock["x"] + dock["width"] <= width
