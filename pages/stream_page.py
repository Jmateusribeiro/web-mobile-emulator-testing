"""
Module containing classes and locators for interacting with the StreamPage.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage



class StreamPageLocators:
    """
    Locators for elements on the StreamPage.
    """
    stream_live: tuple = (By.CSS_SELECTOR, "video")
    btn_accept_video: tuple = (By.CSS_SELECTOR, "button[data-a-target*='start-watching-button']")


class StreamPage(BasePage):
    """
    Class representing the Twitch Stream Page.
    """

    def __init__(self, driver: webdriver.Remote) -> None:
        """
        Initialize StreamPage with driver.

        Args:
            driver (webdriver.Remote): Selenium WebDriver instance.
        """
        super().__init__(driver)

    def handle_video_banner(self) -> None:
        """
        Accept video banner if it appears.

        Returns:
            None
        """
        if self.check_if_element_exists(StreamPageLocators.btn_accept_video):
            self.click_element(StreamPageLocators.btn_accept_video)

    def wait_to_load_stream(self) -> None:
        """
        Wait for video stream to load.

        Returns:
            None
        """
        
        css_selector = StreamPageLocators.stream_live[1]

        self.wait_for_element_visible(StreamPageLocators.stream_live)
        self.wait_for_script_condition(
            f"return document.querySelector('{css_selector}').readyState >= 3"
        )