"""
conftest module - Simplified to use pytest-selenium built-in features
"""
import os
import base64
import pytest
from selenium import webdriver
from pytest_html import extras
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.stream_page import StreamPage
from config.settings import SUPPORTED_BROWSERS, BASE_URL, SCREENSHOT_PATH
from config.browser_config import create_driver
from config.device_profiles import DEFAULT_DEVICE


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add custom command-line option for pytest.

    Args:
        parser (pytest.Parser): The pytest parser object.
    """
    parser.addoption("--Browser",
                     action="store",
                     default="Chrome",
                     help="browser to run the test")


@pytest.fixture(name='browser')
def get_browser(request: pytest.FixtureRequest) -> str:
    """
    Fixture to retrieve the selected browser from the command-line option.

    Args:
        request (pytest.FixtureRequest): The pytest fixture request object.

    Returns:
        str: The selected browser.
    """
    return request.config.getoption('--Browser')


@pytest.fixture(name='driver', scope='function')
def get_driver(request: pytest.FixtureRequest, browser: str):
    """
    Fixture to create and manage WebDriver instance.
    pytest-selenium will automatically capture screenshots on failure.

    Args:
        request (pytest.FixtureRequest): The pytest fixture request object.
        browser (str): The selected browser.

    Yields:
        WebDriver: Selenium WebDriver instance.
    """
    if browser not in SUPPORTED_BROWSERS:
        raise Exception(f"Browser '{browser}' not supported; supported Browsers: {SUPPORTED_BROWSERS}")
    
    driver = create_driver(browser)
    
    yield driver
    
    driver.quit()


@pytest.fixture(name='home_page')
def get_home_page(driver: webdriver.Remote) -> HomePage:
    """
    Fixture to create HomePage instance with shared driver.

    Args:
        driver (webdriver.Remote): Selenium WebDriver instance.

    Returns:
        HomePage: An instance of the HomePage class.
    """
    return HomePage(driver)


@pytest.fixture(name='search_page')
def get_search_page(driver: webdriver.Remote) -> SearchPage:
    """
    Fixture to create SearchPage instance with shared driver.

    Args:
        driver (webdriver.Remote): Selenium WebDriver instance.

    Returns:
        SearchPage: An instance of the SearchPage class.
    """
    return SearchPage(driver)


@pytest.fixture(name='stream_page')
def get_stream_page(driver: webdriver.Remote) -> StreamPage:
    """
    Fixture to create StreamPage instance with shared driver.

    Args:
        driver (webdriver.Remote): Selenium WebDriver instance.

    Returns:
        StreamPage: An instance of the StreamPage class.
    """
    return StreamPage(driver)


# ========== pytest-html customization ==========

def pytest_configure(config: pytest.Config) -> None:
    """
    Configure pytest with custom metadata for HTML reports.

    Args:
        config (pytest.Config): Pytest configuration object.
    """
    config._metadata = {
        'Browser': config.getoption('--Browser'),
        'Base URL': BASE_URL,
        'Test Device': DEFAULT_DEVICE.name,
        'Device Resolution': f"{DEFAULT_DEVICE.width}x{DEFAULT_DEVICE.height}",
        'Pixel Ratio': DEFAULT_DEVICE.pixel_ratio
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Hook to attach screenshots and browser logs to HTML report.
    Filters out verbose logs and captures failure screenshots.

    Args:
        item: pytest test item.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Filter out verbose logs from the report
    if hasattr(report, 'sections'):
        # Remove all captured logs, stdout, stderr from the report
        report.sections = []
    
    # Use 'extras' instead of deprecated 'extra'
    extras_list = getattr(report, "extras", [])
    
    if report.when == "call":
        driver = item.funcargs.get('driver')
        
        if driver:
            if report.failed:
                # Capture failure screenshot
                screenshot = driver.get_screenshot_as_base64()
                extras_list.append(extras.image(screenshot, "Failure Screenshot", mime_type="image/png"))
                
                # Capture browser console logs (only last 10)
                try:
                    logs = driver.get_log('browser')
                    if logs:
                        log_text = '\n'.join([f"[{log['level']}] {log['message']}" for log in logs[-10:]])
                        extras_list.append(extras.text(log_text, "Browser Console Logs"))
                except:
                    pass
            elif report.passed:
                # Include all screenshots from evidences folder for passed tests
                try:
                    if os.path.exists(SCREENSHOT_PATH):
                        # Get all PNG files from evidences folder
                        screenshot_files = sorted([
                            f for f in os.listdir(SCREENSHOT_PATH) 
                            if f.endswith('.png')
                        ])
                        
                        if screenshot_files:
                            # Add each screenshot to the report
                            for screenshot_file in screenshot_files:
                                filepath = os.path.join(SCREENSHOT_PATH, screenshot_file)
                                with open(filepath, 'rb') as f:
                                    screenshot_data = base64.b64encode(f.read()).decode()
                                    # Use filename as label
                                    label = screenshot_file.replace('.png', '').replace('_', ' ').title()
                                    extras_list.append(extras.image(screenshot_data, label, mime_type="image/png"))
                except Exception as e:
                    # If anything fails, take a final screenshot as fallback
                    screenshot = driver.get_screenshot_as_base64()
                    extras_list.append(extras.image(screenshot, "Test Passed Screenshot", mime_type="image/png"))
    
    report.extras = extras_list