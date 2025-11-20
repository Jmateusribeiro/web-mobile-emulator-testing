"""
base_page module
"""
import os
import logging
from typing import Any, Optional
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException, 
    ElementClickInterceptedException, 
    TimeoutException
)
from selenium.webdriver.common.by import By
from config.settings import SCREENSHOT_PATH, DEFAULT_WAIT_TIMEOUT

class BasePageLocators:
    """
    Locators for common elements across pages can be defined here if needed.
    """
    loading_spinner: tuple = (By.CSS_SELECTOR, "[data-a-target='loading-spinner']")

class BasePage:
    """
    Base class for all page objects.
    Accepts a WebDriver instance and provides common page interaction methods.
    """

    def __init__(self, driver: webdriver.Remote, screenshot_path: str = SCREENSHOT_PATH) -> None:
        """
        Initialize the BasePage instance.

        Args:
            driver (webdriver.Remote): Selenium WebDriver instance.
            screenshot_path (str): The path to save screenshots.
        """
        self.driver = driver
        self.screenshot_path = screenshot_path
        self.implicit_wait = DEFAULT_WAIT_TIMEOUT
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_element(self, by_locator: tuple[By, str]) -> WebElement:
        """
        Get the web element identified by the locator.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.

        Returns:
            WebElement: The web element.
        """
        return WebDriverWait(self.driver,
                self.implicit_wait).until(EC.visibility_of_element_located(by_locator))

    def get_element_text(self, by_locator: tuple[By, str]) -> str:
        """
        Get the text of the web element identified by the locator.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.

        Returns:
            str: The text of the web element.
        """
        return self.get_element(by_locator).text

    def type_element(self, by_locator: tuple[By, str], text: str) -> None:
        """
        Type text into the web element identified by the locator.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.
            text (str): The text to type into the web element.

        Returns:
            None
        """
        self.logger.info(f"Typing into element: {by_locator} with text: {text}")
        self.get_element(by_locator).send_keys(text)
        self.logger.info(f"Successfully typed into element: {by_locator}")

    def click_element(self, by_locator: tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        Click on the web element identified by the locator.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.
            timeout (int, optional): Custom timeout in seconds. Defaults to implicit_wait if None.

        Returns:
            None
        """
        self.logger.info(f"Clicking element: {by_locator}")
        timeout = timeout or self.implicit_wait
        element = WebDriverWait(self.driver, timeout).until(
        EC.element_to_be_clickable(by_locator)
        )
        element.click()
        self.logger.info(f"Successfully clicked element: {by_locator}")
    
    def click_web_element(self, element: WebElement) -> None:
        """
            Click a WebElement that's already been found

            Args:
                element (WebElement): The web element to click.

            Returns:
                None    
        """
        self.logger.info(f"Clicking element: {element}")
        
        WebDriverWait(self.driver, self.implicit_wait).until(
            lambda d: element.is_displayed() and element.is_enabled()
        )
        element.click()

        self.logger.info(f"Successfully clicked element: {element}")
   


    def send_keys(self, by_locator: tuple[By, str], key: str | Keys) -> None:
        """
        Send keys to the web element identified by the locator.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.
            key (str | Keys): The keys to send.

        Returns:
            None
        """
        self.logger.info(f"Sending keys to element: {by_locator} with keys: {key}")
        self.get_element(by_locator).send_keys(key)
        self.logger.info(f"Successfully sent keys to element: {by_locator}")

    def is_element_visible(self, by_locator: tuple[By, str]) -> bool:
        """
        Check if the web element identified by the locator is visible.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.

        Returns:
            bool: True if the element is visible, False otherwise.
        """
        return self.get_element(by_locator).is_displayed()

    def check_if_element_exists(self, by_locator: tuple[By, str]) -> bool:
        """
        Check if the web element identified by the locator exists.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        try:
            self.get_element(by_locator)
            return True

        except (NoSuchElementException, TimeoutException):
            return False

    def find_elements(self, by_locator: tuple[By, str]) -> list[WebElement]:
        """
        Find all web elements identified by the locator.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.

        Returns:
            list[WebElement]: List of web elements.
        """
        return self.driver.find_elements(*by_locator)

    def take_screenshot(self, name: str) -> str:
        """
        Take a screenshot and save it with the given name.

        Args:
            name (str): The name to save the screenshot.

        Returns:
            str: Path to the saved screenshot file.
        """
        screenshot_file = os.path.join(self.screenshot_path, f"{name}.png")
        self.driver.save_screenshot(screenshot_file)
        self.logger.info(f"Screenshot saved: {screenshot_file}")
        return screenshot_file

    def wait_for_loading_spinner(self) -> None:
        """
        Wait for the page to fully load.

        Returns:
            None
        """
        WebDriverWait(self.driver, self.implicit_wait).until(
            EC.invisibility_of_element_located(BasePageLocators.loading_spinner)
        )


    def scroll_to_bottom(self) -> None:
        """
        Scroll to the bottom of the page and wait for content to load.

        This method scrolls to the bottom of the page and then waits for
        the loading spinner to disappear, ensuring content is fully loaded.

        Returns:
            None
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.wait_for_loading_spinner()


    def scroll_to_element(self, by_locator: tuple[By, str]) -> None:
        """
        Scroll to make element visible and wait for loading to complete.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.

        Returns:
            None
        """
        element = self.get_element(by_locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.wait_for_loading_spinner()

    def wait_for_url_contains(self, text: str) -> None:
        """
        Wait until the current URL contains the specified text.

        Args:
            text (str): The text to wait for in the URL.

        Returns:
            None
        """
        WebDriverWait(self.driver, self.implicit_wait).until(
            EC.url_contains(text)
        )

    def wait_for_url_to_be(self, url: str) -> None:
        """
        Wait until the current URL matches exactly.

        Args:
            url (str): The exact URL to wait for.

        Returns:
            None
        """
        WebDriverWait(self.driver, self.implicit_wait).until(
            EC.url_to_be(url)
        )
    
    def wait_for_element_visible(self, by_locator: tuple[By, str]) -> None:
        """
        Wait for element to be visible.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.

        Returns:
            None
        """

        WebDriverWait(self.driver, self.implicit_wait).until(
            EC.visibility_of_element_located(by_locator)
        )

    def wait_for_element_invisible(self, by_locator: tuple[By, str]) -> None:
        """
        Wait for element to be invisible.

        Args:
            by_locator (tuple[By, str]): The locator strategy and value.

        Returns:
            None
        """

        WebDriverWait(self.driver, self.implicit_wait).until(
            EC.invisibility_of_element_located(by_locator)
        )

    def execute_javascript(self, script: str, *args) -> Any:
        """
        Execute JavaScript code in the browser.

        Args:
            script (str): The JavaScript code to execute.
            *args: Optional arguments to pass to the script.

        Returns:
            Any: The return value of the script.
        """
        return self.driver.execute_script(script, *args)
    
    def wait_for_script_condition(self, script: str) -> None:
        """
        Wait for a JavaScript condition to become true.

        Args:
            script (str): The JavaScript code that returns a boolean condition.

        Returns:
            None
        """
        WebDriverWait(self.driver, self.implicit_wait).until(
            lambda driver: driver.execute_script(script)
        )