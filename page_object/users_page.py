from page_object import common_page
from page_object.common_page import CommonPage
from utilites.element_interactions import ElementInteractions
from utilites import file_handling as fh
from utilites import logger as log
import time

logger = log.setup_logger("users_page")

class UsersPage:

    def __init__(self, page):
        # page objects
        self.page = page
        self.ei = ElementInteractions(self.page)
        self.common_page = CommonPage(self.page)
        self.add_new_user = "[value='Add New User']"
        self.username="[name='username']"
        self.password = "[name='passwordText']"
        self.retype_password = "[name='passwordTextRetype']"
        self.access = "[name='active']"
        self.firstname="[name='firstName']"
        self.lastname="[name='lastName']"
        self.create_user="[value*='Create User']"
        self.message = "(//*[contains(@class,'msg')])[1]"


    def add_new_user(self):
        """
        ************************************************************
        Author: Nagaraju B
        Creation Date: Oct 2026
        Purpose: Click on Add New User button and verify the form.
        ************************************************************
        """
        current_function_name = fh.get_function_name()

        try:
            self.ei.wait_for_page_timeout(3)
            self.ei.wait_for_page_load()

            if not self.ei.is_visible("css", self.add_new_user):
                self.common_page.navigate_to_module("Users", None)

            if self.ei.is_visible("css", self.add_new_user):
                self.ei.click("css", self.add_new_user)

            self.ei.wait_for_page_timeout(2)

            if not self.ei.is_visible("css", self.username):
                raise AssertionError("Username field is not visible after clicking Add New User.")

            logger.info(f"Function: {current_function_name} - Successfully opened Add New User form.")

        except Exception as e:
            error_msg = (
                f"Function: {current_function_name} - "
                f"Failed to open Add New User form. Reason: {e}"
            )
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from e


    def specify_login_information(self, username, password, access_level):
        """
        ************************************************************
        Author: Nagaraju B
        Creation Date: Oct 2026
        Purpose: This function will help us to fill info in specify login information section
        ************************************************************
        """
        current_function_name = fh.get_function_name()

        try:
            self.ei.enter_text("css", self.username, username)
            self.ei.enter_text("css", self.password, password)
            self.ei.enter_text("css", self.retype_password, password)

            if access_level is not None:
                self.ei.select_item("css", self.access, access_level)

            logger.info(
                f"Function: {current_function_name} - "
                f"Successfully entered login information for user '{username}'."
            )

        except Exception as e:
            error_msg = (
                f"Function: {current_function_name} - "
                f"Failed to enter login information for user '{username}'. "
                f"Reason: {e}"
            )
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from e


    def specify_personal_information(self, firstname, lastname):
        """
        ************************************************************
        Author: Nagaraju B
        Creation Date: Oct 2026
        Purpose: This function will help us to fill info in specify login personal section
        ************************************************************
        """
        current_function_name = fh.get_function_name()

        try:
            self.ei.enter_text("css", self.firstname, firstname)
            self.ei.enter_text("css", self.lastname, lastname)

            logger.info(
                f"Function: {current_function_name} - "
                f"Successfully entered personal information."
            )

        except Exception as e:
            error_msg = (
                f"Function: {current_function_name} - "
                f"Failed to enter personal information. Reason: {e}"
            )
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from e


    def user_creation(self, username, password, access_level, firstname, lastname,create_user_scenario):
        """
        ************************************************************
        Author: Nagaraju B
        Creation Date: Oct 2026
        Purpose: This function will help to create the user
        Return values
        1 - > Success
        2 -> Error
        3 -> Duplicate
        ************************************************************
        """
        current_function_name = fh.get_function_name()

        try:

            UsersPage.add_new_user(self)

            if create_user_scenario.lower().strip()!="do_not_provide_data":

                UsersPage.specify_login_information(self,username, password, access_level)

                UsersPage.specify_personal_information(self,firstname, lastname)

            self.ei.click("css", self.create_user)

            actual_text = self.ei.get_inner_text("xpath", self.message).lower()

            success_exp_text = fh.read_ini_file("users", "success_msg").lower()

            without_filling_exp_text = fh.read_ini_file("users", "without_filling_msg").lower()

            duplicate_exp_text = fh.read_ini_file("users", "duplicate_error_msg").lower()

            if actual_text==success_exp_text:
                intResult = 1
            elif without_filling_exp_text in actual_text:
                intResult = 2
            elif duplicate_exp_text in actual_text:
                intResult = 3
            else:
                intResult = 4

            logger.info(
                f"Function: {current_function_name} - "
                f"Successfully completed user  functionality '{username}'."
            )

            return intResult

        except Exception as e:
            error_msg = (
                f"Function: {current_function_name} - "
                f"Failed to create user '{username}'. Reason: {e}"
            )
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from e

