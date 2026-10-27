from utilites.element_interactions import ElementInteractions
from dotenv import load_dotenv
import os
from utilites import file_handling as fh
load_dotenv()
from utilites import logger as log

logger = log.setup_logger("users_page")

class CommonPage:

    def __init__(self, page):
        # page objects
        self.page = page
        self.ei = ElementInteractions(self.page)
        self.username = "input[name='username']"
        self.password = "input[name='pwd']"
        self.login_button = "input[value*='Login now']"
        self.logout = "img[class='logoutImg']"
        self.logout_verify = "img[class='logoutImg12333']"
        # module navigations
        self.parent_report = "//*[text()='Reports']"
        self.sub_menu_billing_summary_report = "//*[text()='Reports']"
        self.sub_menu_overtime_report = "//*[text()='Overtime Report']"
        self.parent_menu_Users= "//*[text()='Users']"


    def login_to_application(self):
        """
        *********************************************************************
        Author        : B. Nagaraju
        Creation Date : Oct 2026
        Purpose       : Log into the application using configured credentials.
        *********************************************************************
        """
        current_function_name = fh.get_function_name()

        try:
            user_name = os.getenv("APP_USERNAME")
            password = os.getenv("APP_PASSWORD")

            # Validate credentials before interacting with the page.
            if not user_name or not password:
                raise ValueError(
                    "APP_USERNAME or APP_PASSWORD is missing or empty."
                )

            self.ei.enter_text("css", self.username, user_name)
            self.ei.enter_text("css", self.password, password)
            self.ei.click("css", self.login_button)

            self.ei.wait_for_page_load()

            logger.info(
                f"Function: {current_function_name} - "
                f"Login action completed successfully."
            )

        except Exception as exc:
            error_msg = (
                f"Function: {current_function_name} - Failed to log in to the application. Reason: {exc}")
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exc

    def logout_from_application(self):
        """
        *********************************************************************
        Author        : B. Nagaraju
        Creation Date : Oct 2026
        Purpose       : Log out of the application.
        *********************************************************************
        """
        current_function_name = fh.get_function_name()

        try:
            self.ei.click("css", self.logout)

            logger.info(
                f"Function: {current_function_name} - Logout action completed successfully.")

        except Exception as exc:
            error_msg = (
                f"Function: {current_function_name} - "
                f"Failed to log out of the application. Reason: {exc}"
            )
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exc

    def navigate_to_module(self, parent_menu, sub_menu=None):
        """
        *********************************************************************
        Author        : B. Nagaraju
        Creation Date : Oct 2026
        Purpose       : Navigate to a parent menu and optional submenu.
        Input Help:
            parent_menu: Parent menu name, e.g. 'Report' or 'Users'.
            sub_menu: Submenu name, or None if no submenu is required.
        *********************************************************************
        """
        current_function_name = fh.get_function_name()

        obj_parent_menu = ""
        obj_sub_menu = ""

        try:
            match parent_menu.lower().strip():
                case "report":
                    obj_parent_menu = self.parent_report
                    match sub_menu.lower().strip():
                        case "billing summary report":
                            obj_sub_menu = self.sub_menu_billing_summary_report
                        case "overtime report":
                            obj_sub_menu = self.sub_menu_overtime_report
                        case _:
                            raise ValueError(f"Unsupported submenu '{sub_menu}' for parent menu '{parent_menu}'.")
                case "users":
                    obj_parent_menu = self.parent_menu_Users
                case _:
                    raise ValueError(f"Unsupported parent menu '{parent_menu}'.")

            # Verify that the parent menu has an href.
            parent_link = self.ei.get_attribute("xpath", obj_parent_menu, "href")

            if parent_link is not None:
                self.ei.click("xpath", obj_parent_menu)

            # Navigate to the submenu only when sub menu is present in parent menu
            if sub_menu is None:
                logger.info(f"sub_menu is not present in parent menu {obj_parent_menu}")
            else:
                submenu_link = self.ei.get_attribute("xpath",obj_sub_menu,"href")
                if submenu_link is None:
                    logger.info(f"sub_menu {sub_menu} is already clicked ")
                else:
                    self.ei.click("xpath", obj_sub_menu)

            logger.info(
                f"Function: {current_function_name} successfully completed navigation")

        except Exception as exc:
            error_msg = f"Function: {current_function_name} - Error in Navigation - Reason: {exc}"
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exc
