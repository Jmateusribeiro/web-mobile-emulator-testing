"""
conftest module - Using pytest-selenium built-in features
"""
import os
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from pytest_html import extras
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.stream_page import StreamPage
from config.settings import BASE_URL, SCREENSHOT_PATH
from config.browser_config import get_chrome_mobile_options, get_edge_mobile_options
from config.device_profiles import DEFAULT_DEVICE


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add custom command-line options for pytest.

    Args:
        parser (pytest.Parser): The pytest parser object.
    """
    parser.addoption("--Browser",
                     action="store",
                     default="Chrome",
                     help="browser to run the test")


def pytest_configure(config: pytest.Config) -> None:
    """
    Configure pytest with custom metadata and sync pytest-selenium's --driver with --Browser.

    Args:
        config (pytest.Config): Pytest configuration object.
    """

    browser = config.getoption('--Browser')
    driver = config.getoption('--driver', default=None)

    if driver is None:
        config.option.driver = browser


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


@pytest.fixture
def chrome_options():
    """
    Fixture to provide Chrome options with mobile emulation.
    pytest-selenium automatically uses this for Chrome driver.

    Returns:
        ChromeOptions: Chrome options with mobile emulation configured.
    """
    return get_chrome_mobile_options()


@pytest.fixture
def edge_options():
    """
    Fixture to provide Edge options with mobile emulation.
    pytest-selenium automatically uses this for Edge driver.

    Returns:
        EdgeOptions: Edge options with mobile emulation configured.
    """
    return get_edge_mobile_options()


@pytest.fixture(name='driver')
def get_driver(selenium):
    """
    Alias fixture for pytest-selenium's selenium fixture.

    This provides a 'driver' name for compatibility with existing page object fixtures,
    while letting pytest-selenium handle the actual driver creation with chrome_options/edge_options.

    Args:
        selenium: pytest-selenium's built-in selenium fixture.

    Returns:
        WebDriver: Selenium WebDriver instance managed by pytest-selenium.
    """
    return selenium


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

def pytest_html_report_title(report):
    """
    Customize the HTML report title.

    Args:
        report: The HTML report object.
    """
    report.title = "Twitch Mobile Test Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Hook to customize HTML report with browser logs and screenshots as links.

    This hook modifies both failure and success screenshots to be clickable links
    instead of embedded images for better viewing of full-resolution screenshots.

    Args:
        item: pytest test item.
    """
    outcome = yield
    report = outcome.get_result()

    if hasattr(report, 'sections'):
        report.sections = []

    extras_list = getattr(report, "extras", [])

    if report.when == "call":
        driver = item.funcargs.get('driver')

        if driver:
            if report.failed:
                # Add browser console logs for debugging
                try:
                    logs = driver.get_log('browser')
                    if logs:
                        log_text = '\n'.join([f"[{log['level']}] {log['message']}" for log in logs[-20:]])
                        extras_list.append(extras.text(log_text, "Browser Console Logs"))
                except (WebDriverException, KeyError):
                    # Some drivers don't support log retrieval
                    pass

            elif report.passed:
                # Attach custom evidence screenshots as clickable links
                try:
                    if os.path.exists(SCREENSHOT_PATH):
                        screenshot_files = sorted([
                            f for f in os.listdir(SCREENSHOT_PATH)
                            if f.endswith('.png')
                        ])

                        for screenshot_file in screenshot_files:
                            # Create relative path from report to screenshot
                            relative_path = os.path.join('evidences', screenshot_file)
                            label = screenshot_file.replace('.png', '').replace('_', ' ').title()
                            link_html = f'<a href="{relative_path}" target="_blank">{label} (click to view full screenshot)</a>'
                            extras_list.append(extras.html(link_html))
                except (OSError, IOError):
                    # If evidence folder doesn't exist or can't be read, skip custom screenshots
                    pass

    report.extras = extras_list