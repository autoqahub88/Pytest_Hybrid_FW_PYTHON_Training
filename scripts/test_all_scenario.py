
import time
from utilites import logger as log
from playwright.sync_api import sync_playwright, expect

logger = log.setup_logger("test_all_scenario")
class TestAllScenario:

    def test_create_user_with_mandatory_fields(self):

        with (sync_playwright() as p):
            browser = p.chromium.launch(channel="chrome", headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto("http://127.0.0.1/login.do")
            time.sleep(1)
            page.locator("[name='username']").fill("admin")
            page.locator("[name='pwd']").fill("manager")
            page.locator("[value*='Login now']").click()

            with page.expect_response("**/staffoutput.do") as res:
                page.get_by_role("link", name="Reports").click()
            response = res.value
            print(response.status)

            radio_button_all = page.locator("#users_all")
            print("Radio button is -> users_all :", radio_button_all.is_checked())

            with page.expect_download() as res:
                page.locator("[name='genCSV']").click()
            download = res.value
            file_name = download.suggested_filename
            download.save_as(f"./downloaded_files/{file_name}")


            radio_button_user_selected = page.locator("#users_selected")
            print("Radio button users_selected:", radio_button_user_selected.is_checked())

            if not radio_button_user_selected.is_checked():
                time.sleep(3)
                page.on("dialog", lambda dialog: dialog.accept())  ### dismiss , text
                page.locator("[name='genCSV']").click()
                radio_button_user_selected.check()
                page.locator("[name='users']").select_option(index=[0, 2, 4])

            page.locator("[name='firstGrouping']").select_option(["Task names"])

            check_box_showDisabledUsers = page.locator("[name='showDisabledUsers']")
            check_box_showDisabledUsers.scroll_into_view_if_needed()
            time.sleep(1)
            if not check_box_showDisabledUsers.is_checked():
                check_box_showDisabledUsers.check()
                time.sleep(1)
                check_box_showDisabledUsers.uncheck()
                time.sleep(1)

            page.locator("img[name='normalSupportMenuImg']").click()
            old_page = page
            ## popup
            with page.expect_popup() as popup_info:
                page.locator("//div[contains(@onclick,'ReportABug')]").click()
            new_page = popup_info.value
            new_page.locator("#bug").fill("This is a test question.")
            new_page.locator("#emailAddress").fill("Playwright@pl.com")
            new_page.locator("#submitButton").click()
            new_page.close()

            page = old_page
            page.get_by_role("link", name="Projects & Tasks").click()
            table_xpath = "(//b[text()='Filter criteria:']/following::table)[1]/tbody"
            table = page.locator(table_xpath)
            UFT_cell = table.locator("tr", has_text="Test_Test_UFT")
            UFT_cell.locator("//img[contains(@src,'comment_entered.gif')]").click()
            page.locator("[name='comment']").fill("This is a test comment.")
            page.locator("#scbutton").click()

            ## filter
            table_xpath_rows = "(//b[text()='Filter criteria:']/following::table)[1]/tbody/tr"
            cell_text = page.locator(table_xpath_rows).filter(has_text="Test_Test_UFT")
            cell_text.get_by_role("link", name="UFT_U676").click()

            # navigation methods
            page.go_back()
            time.sleep(1)
            page.go_forward()
            time.sleep(1)
            page.go_back()
            time.sleep(1)












