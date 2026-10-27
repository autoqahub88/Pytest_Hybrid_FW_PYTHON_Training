from playwright.sync_api import Page
from utilites import logger as log
from utilites import file_handling as fh

logger = log.setup_logger("element_interaction")

class ElementInteractions:

    def __init__(self, page: Page):
        self.page = page

    def get_locator(self, locator_type, locator_value, **kwargs):
        """
        *****************************************************************************
        Author: Nagaraju B
        Creation Date: Sep 2025
        Purpose: Create a Playwright locator based on locator type and value.
        *****************************************************************************
        """

        locator_type = locator_type.lower().strip()

        match locator_type:

            case "test_id":
                locator = self.page.get_by_test_id(locator_value)

            case "placeholder":
                locator = self.page.get_by_placeholder(locator_value, **kwargs)

            case "role":
                locator = self.page.get_by_role(locator_value, **kwargs)

            case "label":
                locator = self.page.get_by_label(locator_value, **kwargs)

            case "text":
                locator = self.page.get_by_text(locator_value, **kwargs)

            case "alt_text":
                locator = self.page.get_by_alt_text(locator_value, **kwargs)

            case "title":
                locator = self.page.get_by_title(locator_value, **kwargs)

            case "css":
                locator = self.page.locator(f"css={locator_value}", **kwargs)

            case "xpath":
                locator = self.page.locator(f"xpath={locator_value}", **kwargs)

            case _:
                raise ValueError(
                    f"Unsupported locator type: '{locator_type}'. "
                    f"Supported types: test_id, placeholder, role, label, "
                    f"text, alt_text, title, css, xpath."
                )

        return locator

    def enter_text(self,locator_type, locator_value, input_value , **kwargs):
        """
        *****************************************************************************
        Author: Nagaraju B
        Creation Date: Oct 2026
        Purpose: Used to enter text into textbox
        *****************************************************************************
        """
        current_function_name = fh.get_function_name()
        try:
            ElementInteractions.get_locator(self,locator_type, locator_value, **kwargs).fill(input_value)
            logger.info(f"Function-{current_function_name}-Entered text {input_value} into textbox: '{locator_value}'")
        except Exception as exe:
            error_msg = (f"Function-'{current_function_name}'-Failed to enter the text '{locator_value}' into textbox "
                         f"'{locator_value}'.Reason: {exe}")
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exe

    def click(self, locator_type, locator_value, **kwargs):
        """
        ************************************************************
        Author: Nagaraju B
        Creation Date: Oct 2026
        Purpose: Used to click any element.
        **************************************************************
        """
        current_function_name = fh.get_function_name()
        try:
            self.get_locator(locator_type, locator_value,**kwargs).click()
            logger.info(f"Function-{current_function_name}-successfully clicked on : '{locator_value}'")
        except Exception as exe:
            error_msg = (
                f"Function-'{current_function_name}'- Failed to click on '{locator_value}'.Reason: {exe}")
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exe

    def select_item(self, locator_type, locator_value, item_name , **kwargs):
        """
        ************************************************************
        Author: Nagaraju B
        Creation Date: Oct 2026
        Purpose: This function helps to select an item.
        item_name : "Test#Test" -> # is delimeter
        **************************************************************
        """
        current_function_name = fh.get_function_name()

        if item_name.find("#"):
            arr_item = item_name.split("#")
            list_items = [arr_item[cur] for cur in range(len(arr_item))]
        else:
            list_items = item_name

        try:
            self.get_locator(locator_type, locator_value,**kwargs).select_option(list_items)
            logger.info(f"Function-{current_function_name}-successfully selected the item {item_name} in '{locator_value}' dropdown ")
        except Exception as exe:
            error_msg = (f"Function-'{current_function_name}'-Failed to Select the item '{item_name}' into dropdown "
                         f"'{locator_value}'.Reason: {exe}")
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exe

    def is_visible(self, locator_type, locator_value , **kwargs):
        """
        ***************************************************************************************************
        Author        : B. Nagaraju
        Creation Date : Sep 2025
        Purpose       : Checks if the given locator is visible on the page.
        ***************************************************************************************************
        """
        current_function_name = fh.get_function_name()
        try:
            element_visible = ElementInteractions.get_locator(self,locator_type, locator_value , **kwargs).is_visible()
            logger.info(
                f"Function-{current_function_name}- element {locator_value} is visible on page ")
            return element_visible
        except Exception as exe:
            error_msg = (f"Function-'{current_function_name}'-Failed to visible element {locator_value} on the page"
                         f".Reason: {exe}")
            logger.exception(error_msg)
            raise RuntimeError(error_msg) from exe

    def get_attribute(self, locator_type, locator_value , attribute_name, **kwargs):
        """
        ***************************************************************************************************
        Author        : B. Nagaraju
        Creation Date : Sep 2025
        Purpose       : Checks if the given locator is visible on the page.
        ***************************************************************************************************
        """
        try:
            element = ElementInteractions.get_locator(self,locator_type, locator_value , **kwargs)
            return element.get_attribute(attribute_name)
        except Exception as exc:
            # logger.exception(f"[{cur_function_name}] Failed to check visibility for locator '{locator}': {exc}")
            raise RuntimeError(f"[{""}] Error checking visibility for locator'") from exc

    def get_inner_text(self, locator_type, locator_value , **kwargs):
        """
        ***************************************************************************************************
        Author        : B. Nagaraju
        Creation Date : Sep 2025
        Purpose       : Checks if the given locator is visible on the page.
        ***************************************************************************************************
        """
        try:
            element = ElementInteractions.get_locator(self,locator_type, locator_value , **kwargs)
            return element.inner_text()
        except Exception as exc:
            # logger.exception(f"[{cur_function_name}] Failed to check visibility for locator '{locator}': {exc}")
            raise RuntimeError(f"[{""}] Error checking visibility for locator'") from exc


    def wait_for_page_load(self):
        """
        ***********************************************************************************
        Author : Nagaraju B
        Creation Date : Sep 2025
        Purpose : Waits for the page to fully load by checking multiple load states.
        Load states include: 'load', 'networkidle', and 'domcontentloaded'.
        ***********************************************************************************
        """
        try:
            # Wait for different load states sequentially
            self.page.wait_for_load_state("load")
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_load_state("domcontentloaded")
            #self.page.get_by_text("text",exact=True)
        except Exception as e:
            #logger.exception(f"[{cur_function_name}] Unexpected error during page load. Details {str(e)}")
            raise RuntimeError(f"[{""}] Unexpected error during page load.Details {str(e)}") from e

    def wait_for_page_timeout(self,time_out):
        """
        ***********************************************************************************
        Author : Nagaraju B
        Creation Date : Sep 2025
        Purpose : wait for page timeout
        ***********************************************************************************
        """
        try:
            self.page.wait_for_timeout(int(time_out)*1000)
        except Exception as e:
            #logger.exception(f"[{cur_function_name}] Unexpected error during page load. Details {str(e)}")
            raise RuntimeError(f"[{""}] Unexpected error during page load.Details {str(e)}") from e

