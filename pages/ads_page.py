import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AdsPage(BasePage):
    """Page Object for the Ads page."""

    URL = "https://practice-automation.com/ads/"

    # Locators
    PAGE_HEADER = (By.TAG_NAME, "h1")
    INFO_PARAGRAPHS = (By.CSS_SELECTOR, "div.entry-content p")
    AD_MODAL_OVERLAY = (By.ID, "pum-1272")
    AD_MODAL_CONTAINER = (By.ID, "popmake-1272")
    AD_TITLE = (By.ID, "pum_popup_title_1272")
    AD_CONTENT = (By.CSS_SELECTOR, "#popmake-1272 .pum-content p")
    AD_CLOSE_BUTTON = (By.CSS_SELECTOR, "#pum-1272 button.pum-close")

    @allure.step("Open Ads page")
    def load(self) -> None:
        self.open(self.URL)

    @allure.step("Wait for ad modal to appear (up to {timeout} seconds)")
    def wait_for_ad_modal(self, timeout: int = 10) -> bool:
        return self.is_visible(self.AD_MODAL_OVERLAY, timeout=timeout)

    @allure.step("Get ad modal title text")
    def get_ad_title(self) -> str:
        return self.get_text(self.AD_TITLE)

    @allure.step("Get ad modal content text")
    def get_ad_content(self) -> str:
        return self.get_text(self.AD_CONTENT)

    @allure.step("Close ad modal via close button (×)")
    def close_ad(self) -> None:
        self.click(self.AD_CLOSE_BUTTON)

    @allure.step("Check if ad modal is invisible/closed")
    def is_ad_closed(self, timeout: int = 5) -> bool:
        return self.is_invisible(self.AD_MODAL_OVERLAY, timeout=timeout)

    @allure.step("Check if main page content is visible")
    def is_content_visible(self) -> bool:
        return self.is_visible(self.INFO_PARAGRAPHS, timeout=3)
