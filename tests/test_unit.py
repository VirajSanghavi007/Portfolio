"""Unit: single behaviours, with the clock and clipboard mocked."""
import pytest

from conftest import visible_view

FAKE_CLIP_OK = "window.__clip=[]; Object.defineProperty(navigator,'clipboard',{value:{writeText:t=>{window.__clip.push(t);return Promise.resolve()}}});"
FAKE_CLIP_FAIL = "Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('no'))}});"


@pytest.mark.parametrize("when,bar_date,bar_time,w_time,w_date", [
    ("2026-11-12T09:41:00", "Thu 12 Nov", "9:41 AM", "09:41", "Thursday\nNovember 12"),
    ("2026-11-12T00:05:00", "Thu 12 Nov", "12:05 AM", "00:05", "Thursday\nNovember 12"),
    ("2026-03-01T18:30:00", "Sun 1 Mar", "6:30 PM", "18:30", "Sunday\nMarch 1"),
    ("2026-03-01T12:00:00", "Sun 1 Mar", "12:00 PM", "12:00", "Sunday\nMarch 1"),
])
def test_clock_formats(open_page, when, bar_date, bar_time, w_time, w_date):
    page = open_page(fixed_time=when)
    assert page.inner_text("#bar-date") == bar_date
    assert page.inner_text("#bar-time") == bar_time
    assert page.inner_text("#w-time") == w_time
    assert page.eval_on_selector("#w-date", "e => e.innerHTML") == w_date.replace("\n", "<br>")


@pytest.mark.parametrize("view,crumb", [
    ("about", "About me"), ("work", "Projects"), ("resume", "Résumé"), ("contact", "Get in touch"), ("overview", "Overview"),
])
def test_sidebar_switches_view(page, view, crumb):
    page.click(f'.side .nav button[data-view="{view}"]')
    assert visible_view(page) == [view]
    assert page.inner_text("#crumb") == crumb
    current = page.eval_on_selector_all(".side .nav button[aria-current]", "bs => bs.map(b => b.dataset.view)")
    assert current == [view]
    assert page.evaluate("location.hash") == ("" if view == "overview" else "#" + view)


def test_unknown_hash_falls_back_to_overview(open_page):
    page = open_page(hash_="#nope")
    assert visible_view(page) == ["overview"]
    assert page.inner_text("#crumb") == "Overview"


def test_hash_opens_view(open_page):
    page = open_page(hash_="#resume")
    assert visible_view(page) == ["resume"]


def test_copy_email_uses_clipboard(open_page):
    page = open_page(init_script=FAKE_CLIP_OK, hash_="#contact")
    page.click("#copy-email")
    page.wait_for_function("window.__clip.length === 1")
    assert page.evaluate("window.__clip") == ["virajsanghavi000@gmail.com"]
    assert page.inner_text("#toast") == "Copied virajsanghavi000@gmail.com"


def test_copy_email_falls_back_to_selection(open_page):
    page = open_page(init_script=FAKE_CLIP_FAIL, hash_="#contact")
    page.click("#copy-email")
    page.wait_for_function("getSelection().toString().length > 0")
    assert page.evaluate("getSelection().toString()") == "virajsanghavi000@gmail.com"
    assert "selected" in page.inner_text("#toast")


EJS_SRC = "https://cdn.jsdelivr.net/npm/@emailjs/browser@4.4.1/dist/email.min.js"
EJS_OK = "window.__sent=[]; window.emailjs={init:o=>{window.__init=o}, send:(...a)=>{window.__sent.push(a); return Promise.resolve({status:200})}};"
EJS_FAIL = "window.__sent=[]; window.emailjs={init:()=>{}, send:(...a)=>{window.__sent.push(a); return Promise.reject(new Error('402'))}};"
EJS_HANG = "window.__sent=[]; window.emailjs={init:()=>{}, send:(...a)=>{window.__sent.push(a); return new Promise(()=>{})}};"


def stub_emailjs(page, body):
    """Serve a fake EmailJS SDK so nothing is ever really sent; returns the list of SDK requests."""
    hits = []
    def handle(route):
        hits.append(route.request.url)
        if body is None:
            route.abort()
        else:
            route.fulfill(status=200, content_type="application/javascript", body=body)
    page.route(EJS_SRC, handle)
    return hits


def fill_form(page, name="Sam Rivera", email="sam@example.com", text="Hi there"):
    page.fill("#f-name", name)
    page.fill("#f-email", email)
    page.fill("#f-text", text)


def test_form_sends_through_emailjs(open_page):
    page = open_page(hash_="#contact")
    hits = stub_emailjs(page, EJS_OK)
    fill_form(page, name="  Sam Rivera ", text=" Hi there ")
    page.click("#msg-form button[type=submit]")
    page.wait_for_function("document.getElementById('form-note').textContent.startsWith('Sent')")
    assert hits == [EJS_SRC]
    assert page.evaluate("window.__init") == {"publicKey": "0z-U4F7B8BJEgmCHn"}
    assert page.evaluate("window.__sent") == [["service_x4vfqdf", "template_mz5e59w", {
        "name": "Sam Rivera", "email": "sam@example.com", "message": "Hi there", "title": "Portfolio message from Sam Rivera"}]]
    assert page.inner_text("#form-note") == "Sent. Thanks, Sam, I'll reply to sam@example.com."
    assert page.input_value("#f-name") == "" and page.input_value("#f-text") == ""
    assert page.is_enabled("#msg-form button[type=submit]")
    assert page.evaluate("location.hash") == "#contact"  # no navigation


def test_form_sdk_loads_once(open_page):
    page = open_page(hash_="#contact")
    hits = stub_emailjs(page, EJS_OK)
    for i in range(2):
        fill_form(page)
        page.click("#msg-form button[type=submit]")
        page.wait_for_function(f"window.__sent && window.__sent.length === {i + 1}")
    assert hits == [EJS_SRC]
    assert page.locator(f'script[src="{EJS_SRC}"]').count() == 1


def test_form_send_failure_points_to_email(open_page):
    page = open_page(hash_="#contact")
    stub_emailjs(page, EJS_FAIL)
    fill_form(page)
    page.click("#msg-form button[type=submit]")
    page.wait_for_function("document.getElementById('form-note').textContent.startsWith('Couldn')")
    assert page.inner_text("#form-note") == "Couldn't send that, sorry. Please email me at virajsanghavi000@gmail.com."
    assert page.input_value("#f-name") == "Sam Rivera"  # kept for a retry
    assert page.is_enabled("#msg-form button[type=submit]")


def test_form_sdk_load_failure_then_retry(open_page):
    page = open_page(hash_="#contact")
    hits = stub_emailjs(page, None)
    fill_form(page)
    page.click("#msg-form button[type=submit]")
    page.wait_for_function("document.getElementById('form-note').textContent.startsWith('Couldn')")
    page.unroute(EJS_SRC)
    hits2 = stub_emailjs(page, EJS_OK)
    page.click("#msg-form button[type=submit]")
    page.wait_for_function("document.getElementById('form-note').textContent.startsWith('Sent')")
    assert len(hits) == 1 and hits2 == [EJS_SRC]


def test_form_busy_while_sending(open_page):
    page = open_page(hash_="#contact")
    stub_emailjs(page, EJS_HANG)
    fill_form(page)
    page.click("#msg-form button[type=submit]")
    page.wait_for_function("window.__sent && window.__sent.length === 1")
    assert page.inner_text("#form-note") == "Sending…"
    assert page.is_disabled("#msg-form button[type=submit]")
    page.evaluate("document.getElementById('msg-form').requestSubmit()")
    page.wait_for_timeout(100)
    assert page.evaluate("window.__sent.length") == 1


@pytest.mark.parametrize("name,email,text", [("   ", "sam@example.com", "Hi"), ("Sam", "sam@example.com", "   ")])
def test_form_blank_fields_send_nothing(open_page, name, email, text):
    page = open_page(hash_="#contact")
    hits = stub_emailjs(page, EJS_OK)
    fill_form(page, name=name, email=email, text=text)
    page.click("#msg-form button[type=submit]")
    page.wait_for_timeout(150)
    assert hits == [] and page.inner_text("#form-note") == ""


def test_form_needs_fields(open_page):
    page = open_page(hash_="#contact")
    hits = stub_emailjs(page, EJS_OK)
    page.click("#msg-form button[type=submit]")
    assert page.inner_text("#form-note") == ""
    assert hits == []


def test_music_toast_cycles(page):
    page.click('.dock [data-cmd="music"]')
    first = page.inner_text("#toast")
    page.click('.dock [data-cmd="music"]')
    second = page.inner_text("#toast")
    page.click('.dock [data-cmd="music"]')
    assert first != second
    assert page.inner_text("#toast") == first
    assert page.is_visible("#toast.show")


def test_trash_toast(page):
    page.click('.dock [data-cmd="trash"]')
    assert page.inner_text("#toast").startswith("Trash: ")


def test_palette_filters(page):
    page.keyboard.press("Control+k")
    assert page.is_visible("#palette")
    assert page.locator("#palette-list li").count() == 11
    page.fill("#palette-input", "EMAIL")
    assert page.locator("#palette-list li span").all_inner_texts() == ["Copy email address"]
    assert "Nothing matches" not in page.inner_text("#palette-list")
    page.fill("#palette-input", "zzz")
    assert page.locator("#palette-list li").count() == 0
    assert "Nothing matches" in page.inner_text("#palette-list")


def test_palette_arrow_keys_wrap(page):
    page.keyboard.press("Control+k")
    sel = lambda: page.eval_on_selector_all("#palette-list li", "ls => ls.findIndex(l => l.getAttribute('aria-selected') === 'true')")
    assert sel() == 0
    page.keyboard.press("ArrowUp")
    assert sel() == 10
    page.keyboard.press("ArrowDown")
    assert sel() == 0
    page.keyboard.press("ArrowDown")
    assert sel() == 1


def test_palette_escape_and_backdrop_close(page):
    page.keyboard.press("Control+k")
    page.keyboard.press("Escape")
    assert page.is_hidden("#palette")
    page.keyboard.press("Control+k")
    page.mouse.click(10, 860)  # backdrop
    assert page.is_hidden("#palette")
    page.keyboard.press("Control+k")
    page.keyboard.press("Control+k")  # toggles closed
    assert page.is_hidden("#palette")
