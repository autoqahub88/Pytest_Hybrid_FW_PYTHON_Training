import pytest_html
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import pytest
from utilites import file_handling as fh
load_dotenv()


@pytest.fixture(scope="function")
def page():
    """
    ***********************************************************************************
    Author : Nagaraju B
    Creation Date : Oct 2026
    Purpose : Pytest fixture to launch a browser page using Playwright based on configuration
    Reads browser type and headless mode from configuration file.
    ***********************************************************************************
    """
    headless_mode = False
    video_dir = "test-results/videos"
    os.makedirs(video_dir, exist_ok=True)
    browser_name = str(os.getenv("APP_BROWSER"))
    url = str(os.getenv("APP_URL"))
    with sync_playwright() as p:
        try:
            launch_options = {"headless": headless_mode}
            # Launch browser based on config
            match browser_name:
                case "chrome":
                    launch_options["channel"] = "chrome"
                    browser = p.chromium.launch(**launch_options)
                case "edge":
                    launch_options["channel"] = "msedge"
                    browser = p.chromium.launch(**launch_options)
                case "chromium":
                    browser = p.chromium.launch(**launch_options)
                case "firefox":
                    browser = p.firefox.launch(**launch_options)
                case "webkit":   ### safari
                    browser = p.webkit.launch(**launch_options)
                case _:
                    raise ValueError(f"Unsupported browser: {browser_name}")
            # Create browser context and page
            context = browser.new_context(record_video_dir=video_dir)
            page = context.new_page()
            page.goto(url)
            yield page
            page.close()
            browser.close()

        except Exception as e:
            msg = f"Error in page fixture while launching browser -  {browser_name} - setup "
            raise RuntimeError(f"{msg}") from str(e)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    print("outcome",outcome)
    report = outcome.get_result()
    print("report", report)
    print("item", item)
    print("report.when", report.when)
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    yield
    report = request.node.rep_call
    print("request.node.rep_call->", report)
    if report.failed:
        # Create screenshot directory
        screenshot_dir = os.path.join(os.getcwd(),"test-results","screenshots")
        print("screenshot_dir", screenshot_dir)
        os.makedirs(screenshot_dir, exist_ok=True)
        # Create screenshot file name
        test_name = request.node.name+fh.get_timestamp()
        print("test_name", test_name)
        screenshot_path = os.path.join(screenshot_dir,f"{test_name}.png")

        # Capture screenshot and save to file
        page.screenshot(path=screenshot_path,full_page=True)
        # Attach screenshot to pytest-html report
        report.extras.append(
            pytest_html.extras.image(
                screenshot_path
            )
        )


