"""
Test module for Twitch streamer selection functionality.
"""
import pytest



def test_load_streaming(home_page, search_page, stream_page) -> None:
    """
    Test searching for streamers and navigating to channels tab.
    
    Args:
        home_page: HomePage fixture instance.
        search_page: SearchPage fixture instance.
        stream_page: StreamPage fixture instance.
    """
    #homepage
    home_page.open()
    assert home_page.is_loaded(), "Home page did not load correctly"
    
    home_page.handle_cookies_banner()

    #search page
    search_page.search_topic("StarCraft II")
    
    search_page.select_channels_tab()
    
    search_page.scroll_to_bottom()
    search_page.scroll_to_bottom()

    search_page.select_stream_from_results()

    #stream page
    stream_page.handle_video_banner()
    stream_page.wait_to_load_stream()

    stream_page.take_screenshot("stream_page_loaded")