"""
Module containing classes and locators for interacting with the SearchPage.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from selenium.common.exceptions import NoSuchElementException
    


class SearchPageLocators:
    """
    Locators for elements on the SearchPage.
    """
    btn_search: tuple = (By.CSS_SELECTOR, "a[class*='Interactable'][href='/directory']")
    input_search: tuple = (By.CSS_SELECTOR, "[data-a-target='tw-input']")
    tab_channels: tuple = (By.CSS_SELECTOR, "a[href*='type=channels'][role='tab']")
    channels_list: tuple = (By.CSS_SELECTOR, "div[role='list'] > div")
    live_stream_option: tuple = (By.CSS_SELECTOR, "img[src*='/live_user']")


class SearchPage(BasePage):
    """
    Class representing the Twitch Search Page.
    """

    def __init__(self, driver: webdriver.Remote) -> None:
        """
        Initialize SearchPage with driver.

        Args:
            driver (webdriver.Remote): Selenium WebDriver instance.
        """
        super().__init__(driver)

    def search_topic(self, topic_name: str) -> None:
        """
        Search for a topic on Twitch.

        Args:
            topic_name (str): The name of the topic to search for.

        Returns:
            None
        """
        self.click_element(SearchPageLocators.btn_search)
        self.type_element(SearchPageLocators.input_search, topic_name)
        self.send_keys(SearchPageLocators.input_search, Keys.ENTER)

    def select_channels_tab(self) -> None:
        """
        Click on the Channels tab in search results and wait for tab to load.

        Returns:
            None
        """
        self.click_element(SearchPageLocators.tab_channels)
        self.wait_for_url_contains("type=channels")
        self.wait_for_element_visible(SearchPageLocators.channels_list)

    
    def select_stream_from_results(self) -> None:
        """
        Select the first live streaming channel from search results.

        This method attempts to find and click on a live streaming channel up to 3 times,
        scrolling to load more results between attempts if needed.

        Returns:
            None

        Raises:
            Exception: If no live streamers are found after 3 attempts.
        """
        max_attempts = 3
        found_stream = False

        for attempt in range(max_attempts):
            channels = self.find_elements(SearchPageLocators.channels_list)
            
            for channel in channels:
                try:
                    if channel.find_element(*SearchPageLocators.live_stream_option):
                        self.click_web_element(channel)
                        found_stream = True
                        break
                except NoSuchElementException:
                    continue
            
            if found_stream:
                break
            
            if attempt < max_attempts - 1:
                self.scroll_to_bottom()

        if not found_stream:
            raise Exception(f"No live streamers found after {max_attempts} attempts.")
            
        
