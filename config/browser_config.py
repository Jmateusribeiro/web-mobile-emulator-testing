"""
Browser configuration module for test automation
"""
from typing import Union
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from config.device_profiles import DEFAULT_DEVICE, DeviceProfile, to_mobile_emulation


def get_chrome_mobile_options(device: DeviceProfile = DEFAULT_DEVICE) -> ChromeOptions:
    """
    Get Chrome options configured for mobile emulation.

    Args:
        device (DeviceProfile, optional): Device profile to emulate. Defaults to DEFAULT_DEVICE (iPhone 8).

    Returns:
        ChromeOptions: Configured Chrome options with mobile emulation.

    Example:
        >>> from config.device_profiles import PIXEL_7
        >>> options = get_chrome_mobile_options(PIXEL_7)
    """
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", to_mobile_emulation(device))
    return chrome_options


def get_edge_mobile_options(device: DeviceProfile = DEFAULT_DEVICE) -> EdgeOptions:
    """
    Get Edge options configured for mobile emulation.

    Args:
        device (DeviceProfile, optional): Device profile to emulate. Defaults to DEFAULT_DEVICE (iPhone 8).

    Returns:
        EdgeOptions: Configured Edge options with mobile emulation.

    Example:
        >>> from config.device_profiles import IPHONE_14_PRO
        >>> options = get_edge_mobile_options(IPHONE_14_PRO)
    """
    edge_options = EdgeOptions()
    edge_options.add_experimental_option("mobileEmulation", to_mobile_emulation(device))
    return edge_options


def get_headless_chrome_options() -> ChromeOptions:
    """
    Get Chrome options configured for headless mode.

    Returns:
        ChromeOptions: Configured Chrome options for headless execution.
    """
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    return chrome_options


def create_driver(browser_name: str) -> Union[webdriver.Chrome, webdriver.Edge]:
    """
    Create and return a WebDriver instance based on browser name.

    Args:
        browser_name (str): Name of the browser ('Chrome', 'Edge', 'Headless Chrome').

    Returns:
        Union[webdriver.Chrome, webdriver.Edge]: Configured WebDriver instance.

    Raises:
        Exception: If browser is not supported.
    """
    if browser_name == 'Chrome':
        driver = webdriver.Chrome(options=get_chrome_mobile_options())
        return driver
    
    if browser_name == 'Edge':
        return webdriver.Edge(options=get_edge_mobile_options())
    
    #if browser_name == 'Headless Chrome':
    #    return webdriver.Chrome(options=get_headless_chrome_options())
    
    raise Exception(f'Browser "{browser_name}" is not supported. Supported browsers: Chrome, Edge, Headless Chrome')
