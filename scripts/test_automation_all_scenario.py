from pathlib import Path
from playwright.sync_api import Page, expect

def test_automation_practice_all_controls(page: Page) -> None:

    file_path = Path(__file__).resolve().parents[1] / "application/AutomationPractice.html"
    page.goto(str(file_path))
    expect(page.locator("#loginContainer")).to_be_visible()
    expect(page.get_by_role("heading", name="Login")).to_be_visible()
    page.locator("#username").fill("admin")
    page.locator("#password").fill("admin")
    expect(page.locator("#username")).to_have_value("admin")
    expect(page.locator("#password")).to_have_value("admin")
    page.locator("#loginBtn").click()
    expect(page.locator("#loginContainer")).to_be_hidden()
    expect(page.locator("#mainContent")).to_be_visible()
    expect(page.get_by_role("heading", name="Registration Page")).to_be_visible()

    for field, value in {
        "#fullName": "Alex Example",
        "#firstName": "Alex",
        "#middleName": "Taylor",
        "#lastName": "Example",
        "#mobilenumber": "5550100",
        "#emailid": "alex@example.com",
        "#address": "123 Test Street",
    }.items():
        page.locator(field).fill(value)
        expect(page.locator(field)).to_have_value(value)
    expect(page.locator("#tooltipText")).to_have_text("Alex Example")

    page.locator("#countrySelect").select_option("India")
    expect(page.locator("#stateSelect")).to_be_enabled()
    page.locator("#stateSelect").select_option("Karnataka")
    expect(page.locator("#citySelect")).to_be_enabled()
    page.locator("#citySelect").select_option("Bengaluru")
    expect(page.locator("#citySelect")).to_have_value("Bengaluru")

    alpha_frame = page.frame_locator("#frameAlpha")
    alpha_frame.locator("#frameAlphaText").fill("Frame Alpha test")
    expect(alpha_frame.locator("#frameAlphaText")).to_have_value("Frame Alpha test")
    alpha_frame.locator("#frameAlphaSelect").select_option("Alpha Opt 2")
    expect(alpha_frame.locator("#frameAlphaSelect")).to_have_value("Alpha Opt 2")
    inner_frame = page.frame_locator("#frameOuter").frame_locator("#frameInner")
    inner_frame.locator("#innerInput").fill("Nested frame test")
    expect(inner_frame.locator("#innerInput")).to_have_value("Nested frame test")

    page.locator("#dragSource").drag_to(page.locator("#dropZone"))
    expect(page.locator("#dropZone")).to_have_text("Dropped!")
    expect(page.locator("#dragDropStatus")).to_have_text(
        "Drag and drop completed successfully."
    )

    page.locator("#male").check()
    page.locator("#female").check()
    expect(page.locator("#male")).to_be_checked()
    expect(page.locator("#female")).to_be_checked()
    page.get_by_label("Graduation", exact=True).check()
    expect(page.get_by_label("Graduation", exact=True)).to_be_checked()
    page.get_by_label("Post Graduation", exact=True).check()
    expect(page.get_by_label("Post Graduation", exact=True)).to_be_checked()

    page.locator("#district").select_option(label="Mysuru")
    expect(page.locator("#district")).to_have_value("Mysuru")
    with page.expect_popup() as district_tab:
        page.get_by_role("button", name="Open in New Tab").click()
    tab = district_tab.value
    expect(tab.get_by_role("heading", name="Mysuru")).to_be_visible()
    expect(tab.locator("#mainPerson")).to_have_value("Mysuru Main Persona")
    expect(tab.locator("#talukSelect")).to_have_value("Mysuru")
    tab.close()
    with page.expect_popup() as district_window:
        page.get_by_role("button", name="Open in New Window").click()
    window = district_window.value
    expect(window.get_by_role("heading", name="Mysuru")).to_be_visible()
    window.close()

    age = page.locator("#shadowHost").locator("#ageInput")
    age.fill("30")
    expect(age).to_have_value("30")

    course_rows = page.locator("#courseTable tbody tr")
    expect(course_rows).to_have_count(5)
    page.get_by_role("button", name="3 Rows").click()
    expect(course_rows).to_have_count(3)
    page.get_by_role("button", name="5 Rows").click()
    expect(course_rows).to_have_count(5)
    page.get_by_role("button", name="10 Rows").click()
    expect(course_rows).to_have_count(10)

    page.locator("#tableSearch").press_sequentially("Biology")
    expect(page.locator("#courseTable tbody tr:visible")).to_have_count(1)
    expect(page.locator("#courseTable tbody tr:visible")).to_contain_text("Biology")
    page.locator("#tableSearch").press("Control+A")
    page.locator("#tableSearch").press("Backspace")
    expect(page.locator("#courseTable tbody tr:visible")).to_have_count(10)
    course_header = page.locator("#courseTable thead th").first
    course_header.click()
    expect(course_header).to_have_attribute("sort", "asc")
    course_header.click()
    expect(course_header).to_have_attribute("sort", "desc")
    expect(page.locator("#courseTable a")).to_have_count(10)
    for index in range(10):
        row = page.locator("#courseTable tbody tr").nth(index)
        row.locator(".joiningSelect").select_option("Yes")
        expect(row.locator(".joiningSelect")).to_have_value("Yes")
        row.locator(".courseChk").check()
        expect(row.locator(".courseChk")).to_be_checked()
        row.locator('input[type="radio"]').check()
        expect(row.locator('input[type="radio"]')).to_be_checked()
        row.locator(".courseComment1").fill(f"First comment {index}")
        row.locator(".courseComment2").fill(f"Second comment {index}")
        expect(row.locator(".courseComment1")).to_have_value(f"First comment {index}")
        expect(row.locator(".courseComment2")).to_have_value(f"Second comment {index}")

    page.locator("#fileUpload").set_input_files(
        {
            "name": "automation-test.txt",
            "mimeType": "text/plain",
            "buffer": b"Playwright upload test",
        }
    )
    expect(page.locator("#fileUploadDisplay")).to_have_text(
        'file_name = "automation-test.txt"'
    )
    page.locator("#fileUpload").set_input_files(
        {"name": "invalid.exe", "mimeType": "application/octet-stream", "buffer": b"x"}
    )
    expect(page.locator("#fileUploadDisplay")).to_contain_text("Invalid file type")
    expect(page.locator("#fileUpload")).to_have_value("")

    for selector, expected_message in (
        ('button[onclick="showJSAlert()"]', "JavaScript Alert Triggered!"),
        ('button[onclick="showAlertBox()"]', "This is an alert box!"),
    ):
        alert_message = []
        page.once(
            "dialog",
            lambda dialog: (alert_message.append(dialog.message), dialog.accept()),
        )
        page.locator(selector).click()
        assert alert_message == [expected_message]

    page.once("dialog", lambda dialog: dialog.accept(prompt_text="Automated comment"))
    page.locator('button[onclick="showPromptBox()"]').click()
    expect(page.locator("#promptResult")).to_have_text("You said: Automated comment")
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("#confirmBtn").click()
    expect(page.locator("#confirmResult")).to_have_text("You pressed OK")
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.locator("#confirmBtn").click()
    expect(page.locator("#confirmResult")).to_have_text("You pressed Cancel")

    page.locator('button[onclick^="showToast"]').click()
    expect(page.locator("#toastNotification")).to_contain_text(
        "automated toast alert notification"
    )
    page.locator("#doubleClickBtn").dblclick()
    expect(page.locator("#doubleClickResult")).to_contain_text("double-clicked")
    expect(page.locator("#promoCode")).to_have_value("AUTOMATION2026")
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.get_by_role("button", name="Copy Code").click()
    expect(page.locator("#copyStatus")).to_have_text("Code copied to clipboard!")

    page.locator(".navbar li").nth(1).hover()
    page.locator(".dropdown-submenu").filter(has_text="Automation Testing").hover()
    page.locator(".submenu-content a[href='#playwright']").click()
    expect(page.locator("#toastNotification")).to_contain_text("Selected: Playwright")

    page.locator("#calendarInput").click()
    expect(page.locator("#calendarWidget")).to_be_visible()
    page.locator("#calendarMonthSelect").select_option("8")
    page.locator("#calendarYearSelect").select_option("2026")
    page.locator("#calendarDays button").filter(has_text="15").click()
    expect(page.locator("#calendarInput")).to_have_value("15-09-2026")
    page.locator("#dob").fill("01-01-2000")
    expect(page.locator("#dob")).to_have_value("01-01-2000")

    page.locator("#country").fill("Japan")
    expect(page.locator("#country")).to_have_value("Japan")
    page.locator("#satisfaction").press("End")
    expect(page.locator("#satisfactionText")).to_have_value("100")
    page.locator("#satisfactionText").fill("42")
    expect(page.locator("#satisfaction")).to_have_value("42")

    for field, value in (("#colorR", "12"), ("#colorG", "34"), ("#colorB", "56")):
        page.locator(field).fill(value)
    expect(page.locator("#colorPreview")).to_have_css(
        "background-color", "rgb(12, 34, 56)"
    )
    page.locator("#hobbies").select_option(label=["Reading", "Music"])
    expect(page.locator("#hobbiesSelected")).to_have_text(
        "Selected Hobbies: Reading, Music"
    )
    page.locator("label.switch .slider-toggle").click()
    expect(page.locator("#newsletterToggle")).to_be_checked()
    page.locator("#starRating span[data-val='4']").click()
    expect(page.locator("#starRating span.filled")).to_have_count(4)
    expect(page.locator("#disabledField")).to_be_disabled()
    expect(page.locator("#readonlyField")).to_have_value("Read only value")

    accordion = page.locator("#accordionBody")
    page.locator(".accordion-header").click()
    expect(accordion).to_have_class("accordion-body open")
    page.locator(".accordion-header").click()
    expect(accordion).not_to_have_class("accordion-body open")
    for tab_name, panel in (
        ("Profile", "#tab1"),
        ("Preferences", "#tab2"),
        ("Security", "#tab3"),
    ):
        page.get_by_role("button", name=tab_name, exact=True).click()
        expect(page.locator(panel)).to_be_visible()

    page.get_by_role("button", name="Open Modal Dialog").click()
    expect(page.locator("#modalOverlay")).to_be_visible()
    page.locator("#modalOverlay").get_by_role("button", name="Close").click()
    expect(page.locator("#modalOverlay")).to_be_hidden()

    page.get_by_role("button", name="Submit with Loading Spinner").click()
    expect(page.locator("#spinnerEl")).to_be_visible()
    page.once("dialog", lambda dialog: dialog.accept())
    expect(page.locator("#spinnerEl")).to_be_hidden(timeout=5000)

    context_target = page.locator('div[oncontextmenu="showContextMenu(event)"]')
    for action in ("Edit", "Delete", "Share"):
        context_target.click(button="right")
        expect(page.locator("#contextMenu")).to_be_visible()
        dialog_message = []
        page.once(
            "dialog",
            lambda dialog: (dialog_message.append(dialog.message), dialog.accept()),
        )
        page.locator("#contextMenu").get_by_text(action, exact=True).click()
        assert dialog_message == [f"{action} clicked"]
        expect(page.locator("#contextMenu")).to_be_hidden()

    page.get_by_role("button", name="Reveal Hidden Element").click()
    expect(page.locator("#hiddenElement")).to_be_visible()

    page.locator("#fullName").fill("Alex Example")
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Save", exact=True).click()
    expect(page.locator("#downloadArea")).to_be_visible()
    with page.expect_download() as text_download:
        page.get_by_role("button", name="Download TXT").click()
    assert text_download.value.suggested_filename == "registration_summary.txt"

    if page.evaluate("typeof XLSX !== 'undefined'"):
        with page.expect_download() as xlsx_download:
            page.get_by_role("button", name="Download XLSX").click()
        assert xlsx_download.value.suggested_filename == "registration_summary.xlsx"
    else:
        page.once("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name="Download XLSX").click()

    expect(page.locator("a")).to_have_count(26)
    expect(page.locator("a[href]")).to_have_count(26)

    page.get_by_role("button", name="Logout").click()
    expect(page.locator("#mainContent")).to_be_hidden()
    expect(page.locator("#loginContainer")).to_be_visible()
