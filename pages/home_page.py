"""
Module containing classes and locators for interacting with the HomePage.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import BASE_URL


class HomePageLocators:
    """
    Locators for elements on the HomePage.
    """
    home_page_url: str = BASE_URL
    title: str = 'Twitch'
    btn_accept_cookies: tuple = (By.CSS_SELECTOR, "[data-a-target='consent-banner-accept']")
    btn_search: tuple = (By.CSS_SELECTOR, "a[href='/directory']")


class HomePage(BasePage):
    """
    Class representing the Twitch HomePage.
    """

    def __init__(self, driver: webdriver.Remote) -> None:
        """
        Initialize HomePage with driver.

        Args:
            driver (webdriver.Remote): Selenium WebDriver instance.
        """
        super().__init__(driver)
        self.url = HomePageLocators.home_page_url

    def open(self) -> 'HomePage':
        """
        Navigate to the home page.

        Returns:
            HomePage: Returns self for method chaining.
        """
        self.driver.get(self.url)
        return self

    def is_loaded(self) -> bool:
        """
        Verify the home page is loaded correctly.

        Returns:
            bool: True if page title matches expected title.
        """
        return self.driver.title == HomePageLocators.title

    def handle_cookies_banner(self) -> None:
        """
        Accept cookies banner if it appears.

        Returns:
            None
        """
        if self.check_if_element_exists(HomePageLocators.btn_accept_cookies):
            self.click_element(HomePageLocators.btn_accept_cookies)
            self.wait_for_element_invisible(HomePageLocators.btn_accept_cookies)

    def click_search_button(self) -> None:
        """
        Click the search/directory button.

        Returns:
            None
        """
        self.click_element(HomePageLocators.btn_search)
