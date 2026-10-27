import pytest
from page_object.common_page import CommonPage
from page_object.users_page import UsersPage
from utilites import file_handling as fh
from utilites import logger as log

logger = log.setup_logger("test_reports")

@pytest.mark.usefixtures("page")
class TestReports:


    def test_create_user_with_mandatory_fields(self,page):
        """
        *********************************************************************
        Author        : B. Nagaraju
        Creation Date : Oct 2026
        Purpose       : Create user with mandatory fields
        *********************************************************************
        """
        current_test_name = fh.get_function_name()
        try:
            logger.info(f"Started Test Case : {current_test_name}")
            #Step:1 - login to application
            common_page = CommonPage(page)
            common_page.login_to_application()
            excel_data = fh.read_test_data("Users",current_test_name)
            username = excel_data["Username"] + fh.get_timestamp()
            password = excel_data["Password"]
            firstname = excel_data["First_Name"] + fh.get_timestamp()
            lastname = excel_data["Last_Name"] + fh.get_timestamp()
            create_user_scenario = excel_data["create_user_scenario"]
            access_level = None

            # Step:2 - Create User
            users_page = UsersPage(page)
            if users_page.user_creation(username,password,access_level,firstname,
                                        lastname,create_user_scenario)==1:
                logger.info(f"Successfully created user {username}")
            else:
                logger.error(f"Failed to create the user {username}")

            logger.info(f"Completed Test Case : {current_test_name}")
        except Exception as exc:
            error_msg = f"Failed Test Case: {current_test_name} | Reason: {str(exc)}"
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exc


    def test_verify_duplicate_user(self, page):
        """
        *********************************************************************
        Author        : B. Nagaraju
        Creation Date : Oct 2026
        Purpose       : This script helps to verify duplicate users functionality
        *********************************************************************
        """
        current_test_name = fh.get_function_name()
        try:
            logger.info(f"Started Test Case : {current_test_name}")
            # Step:1 - login to application
            common_page = CommonPage(page)
            common_page.login_to_application()
            excel_data = fh.read_test_data("Users", current_test_name)
            username = excel_data["Username"] + fh.get_timestamp()
            password = excel_data["Password"]
            firstname = excel_data["First_Name"] + fh.get_timestamp()
            lastname = excel_data["Last_Name"] + fh.get_timestamp()
            create_user_scenario = excel_data["create_user_scenario"]
            access_level = None

            # Step:2 - Create User
            users_page = UsersPage(page)
            if users_page.user_creation(username, password, access_level, firstname,
                                        lastname, create_user_scenario) == 1:
                logger.info(f"Successfully created the user {username}")
            else:
                logger.error(f"Failed to create the user {username}")

            # step 3 : Duplicate the user
            if users_page.user_creation(username, password, access_level, firstname,
                                        lastname, create_user_scenario) == 3:
                logger.info(f"Successfully verified the duplicate user {username}")
            else:
                logger.error(f"Failed to verify duplicate user {username}")

            logger.info(f"Completed Test Case : {current_test_name}")
        except Exception as exc:
            error_msg = f"Failed Test Case: {current_test_name} | Reason: {str(exc)}"
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exc

    def test_verify_error_message_without_providing_anything(self,page):
        """
        *********************************************************************
        Author        : B. Nagaraju
        Creation Date : Oct 2026
        Purpose       : Create user with mandatory fields
        *********************************************************************
        """
        current_test_name = fh.get_function_name()
        try:
            logger.info(f"Started Test Case : {current_test_name}")
            #Step:1 - login to application
            common_page = CommonPage(page)
            common_page.login_to_application()
            excel_data = fh.read_test_data("Users",current_test_name)
            username = excel_data["Username"] + fh.get_timestamp()
            password = excel_data["Password"]
            firstname = excel_data["First_Name"] + fh.get_timestamp()
            lastname = excel_data["Last_Name"] + fh.get_timestamp()
            create_user_scenario = excel_data["create_user_scenario"]
            access_level = None

            # Step:2 - Create User
            users_page = UsersPage(page)
            if users_page.user_creation(username,password,access_level,firstname,
                                        lastname,create_user_scenario)==2:
                logger.info(f"successfully verified the user is not created by not providing anything"
                            f" {username}")
            else:
                logger.error(f"User is {username} created successfully")

            logger.info(f"Completed Test Case : {current_test_name}")
        except Exception as exc:
            error_msg = f"Failed Test Case: {current_test_name} | Reason: {str(exc)}"
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exc







