"""
conftest module
"""
import os
import logging
from datetime import datetime
import pytest
from selenium import webdriver
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

@pytest.fixture(name='driver')
def get_driver(request: pytest.FixtureRequest, browser: str):
    """
    Fixture to create and manage WebDriver instance.

    Args:
        request (pytest.FixtureRequest): The pytest fixture request object.
        browser (str): The selected browser.

    Yields:
        WebDriver: Selenium WebDriver instance.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Initializing browser: {browser}")
    
    if browser not in SUPPORTED_BROWSERS:
        raise Exception(f"Browser '{browser}' not supported; supported Browsers: {SUPPORTED_BROWSERS}")
    
    # Create driver
    driver = create_driver(browser)
    
    yield driver

    # Teardown
    logger.info("Closing browser")
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


# ========== Pytest Hooks ==========

def pytest_configure(config: pytest.Config) -> None:
    """
    Configure pytest with custom metadata and timestamped reports.

    Args:
        config (pytest.Config): Pytest configuration object.
    """
    # Add custom metadata to HTML report
    config._metadata = {
        'Browser': config.getoption('--Browser'),
        'Base URL': BASE_URL,
        'Test Device': DEFAULT_DEVICE.name,
        'Device Resolution': f"{DEFAULT_DEVICE.width}x{DEFAULT_DEVICE.height}",
        'Pixel Ratio': DEFAULT_DEVICE.pixel_ratio
    }

    # Add timestamped report filename
    if config.option.htmlpath:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_path = config.option.htmlpath.replace('.html', '')
        config.option.htmlpath = f"{base_path}_{timestamp}.html"


def pytest_html_results_table_header(cells):
    """Customize HTML report table header."""
    cells.insert(2, '<th>Description</th>')


def pytest_html_results_table_row(report, cells):
    """Add test description to HTML report table row."""
    if hasattr(report, 'description'):
        cells.insert(2, f'<td>{report.description}</td>')
    else:
        cells.insert(2, '<td></td>')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    Hook to capture screenshots on test failure and attach to HTML report.
    Also embeds test screenshots and filters out verbose logs from HTML report.

    Args:
        item (pytest.Item): Test item.
        call (pytest.CallInfo): Call information.
    """
    outcome = yield
    report = outcome.get_result()

    # Add test description from docstring to report
    if report.when == "call" and item.function.__doc__:
        report.description = item.function.__doc__.strip()

    # Clear only stdout/stderr sections to keep HTML report clean
    # Keep log sections (setup, call, teardown logs) but filter to INFO level only
    if hasattr(report, 'sections'):
        filtered_sections = []
        for name, content in report.sections:
            # Remove stdout/stderr entirely
            if any(keyword in name.lower() for keyword in ['captured stdout', 'captured stderr']):
                continue

            # For log sections, filter to show only INFO and above (exclude DEBUG)
            if 'log' in name.lower():
                # Filter out DEBUG level logs from content
                filtered_lines = [
                    line for line in content.split('\n')
                    if not ('[DEBUG' in line or 'DEBUG]' in line)
                ]
                filtered_content = '\n'.join(filtered_lines).strip()
                if filtered_content:  # Only add if content remains after filtering
                    filtered_sections.append((name, filtered_content))
            else:
                filtered_sections.append((name, content))

        report.sections = filtered_sections

    # Attach screenshots to HTML report (both manual and failure screenshots)
    if report.when == "call":
        extra = getattr(report, 'extra', [])
        if extra is None:
            extra = []

        try:
            # Find all screenshots in evidences folder for this test
            if os.path.exists(SCREENSHOT_PATH):
                # Get all PNG files in the screenshot directory
                all_screenshots = [f for f in os.listdir(SCREENSHOT_PATH) if f.endswith('.png')]

                # Attach screenshots taken during test (manual screenshots)
                for screenshot_file in all_screenshots:
                    screenshot_full_path = os.path.join(SCREENSHOT_PATH, screenshot_file)
                    # Check if file was created recently (during this test run)
                    file_age = datetime.now().timestamp() - os.path.getmtime(screenshot_full_path)
                    if file_age < 60:  # Created in last 60 seconds
                        relative_path = os.path.relpath(screenshot_full_path,
                                                        os.path.dirname(item.config.option.htmlpath))
                        extra.append({
                            'name': f'Screenshot: {screenshot_file}',
                            'format': 'image',
                            'content': relative_path,
                            'mime_type': 'image/png'
                        })
        except Exception as e:
            logging.getLogger(__name__).debug(f"Error checking screenshots: {e}")

        # Capture screenshot on failure
        if report.failed:
            driver = item.funcargs.get('driver')
            if driver:
                try:
                    # Generate screenshot filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_name = f"{item.name}_failure_{timestamp}"
                    screenshot_path = os.path.join(SCREENSHOT_PATH, f"{screenshot_name}.png")

                    # Save screenshot
                    driver.save_screenshot(screenshot_path)

                    # Add failure screenshot to HTML report
                    relative_path = os.path.relpath(screenshot_path,
                                                    os.path.dirname(item.config.option.htmlpath))
                    extra.append({
                        'name': 'Failure Screenshot',
                        'format': 'image',
                        'content': relative_path,
                        'mime_type': 'image/png'
                    })

                    # Log to file and console (NOT to HTML report sections)
                    logging.getLogger(__name__).info(f"Failure screenshot saved: {screenshot_path}")
                except Exception as e:
                    logging.getLogger(__name__).error(f"Failed to capture screenshot: {e}")

        # Assign extras back to report
        if extra:
            report.extra = extra