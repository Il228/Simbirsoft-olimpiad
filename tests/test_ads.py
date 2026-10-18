import allure
import pytest
import time
from pages.ads_page import AdsPage


@allure.epic("UI Automation Practice")
@allure.feature("Ads Page")
class TestAds:
    """Test suite for Ads page functionality."""

    @pytest.mark.positive
    @pytest.mark.ads
    @allure.story("Page Display")
    @allure.title("AP-01: Verify initial page elements and ad description are displayed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ads_page_elements_loaded(self, driver):
        """Verifies initial page loads with instructions about ad display."""
        page = AdsPage(driver)
        page.load()

        assert page.is_content_visible(), "Page description and content should be visible"

    @pytest.mark.positive
    @pytest.mark.ads
    @allure.story("Ad Modal Display")
    @allure.title("AP-02: Ad modal appears automatically after timed delay")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ad_modal_appears_automatically(self, driver):
        """Verifies ad modal triggers and appears after the configured delay."""
        page = AdsPage(driver)
        page.load()

        assert page.wait_for_ad_modal(timeout=10), "Ad modal should appear automatically within 10 seconds"

    @pytest.mark.positive
    @pytest.mark.ads
    @allure.story("Ad Modal Content")
    @allure.title("AP-03: Verify ad modal title is 'Hi'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_modal_title(self, driver):
        """Verifies title text of the ad popup."""
        page = AdsPage(driver)
        page.load()

        page.wait_for_ad_modal(timeout=10)
        assert page.get_ad_title() == "Hi", "Ad title should be 'Hi'"

    @pytest.mark.positive
    @pytest.mark.ads
    @allure.story("Ad Modal Content")
    @allure.title("AP-04: Verify ad modal content contains 'I am an ad.'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_modal_content(self, driver):
        """Verifies body text of the ad popup."""
        page = AdsPage(driver)
        page.load()

        page.wait_for_ad_modal(timeout=10)
        assert "I am an ad." in page.get_ad_content(), "Ad body should contain 'I am an ad.'"

    @pytest.mark.positive
    @pytest.mark.ads
    @allure.story("Ad Dismissal")
    @allure.title("AP-05: Close ad modal using close button (×)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_close_ad_modal(self, driver):
        """Verifies clicking close button closes the ad modal."""
        page = AdsPage(driver)
        page.load()

        page.wait_for_ad_modal(timeout=10)
        page.close_ad()
        assert page.is_ad_closed(), "Ad modal should be closed after clicking close button"

    @pytest.mark.positive
    @pytest.mark.ads
    @allure.story("Page Usability")
    @allure.title("AP-06: Page content is fully usable after closing ad")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_usable_after_closing_ad(self, driver):
        """Verifies background content is accessible and readable once ad is dismissed."""
        page = AdsPage(driver)
        page.load()

        page.wait_for_ad_modal(timeout=10)
        page.close_ad()
        assert page.is_content_visible(), "Page content should remain visible and accessible"

    @pytest.mark.positive
    @pytest.mark.ads
    @allure.story("Ad Dismissal")
    @allure.title("AP-07: Ad modal overlay is completely hidden after closing")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_overlay_hidden_after_close(self, driver):
        """Verifies ad modal overlay is removed/hidden from the viewport."""
        page = AdsPage(driver)
        page.load()

        page.wait_for_ad_modal(timeout=10)
        page.close_ad()
        assert not page.is_visible(page.AD_MODAL_OVERLAY, timeout=2), "Ad overlay should not be visible"

    # ================= NEGATIVE TESTS =================

    @pytest.mark.negative
    @pytest.mark.ads
    @allure.story("Timing & State")
    @allure.title("AN-01: Ad modal is NOT visible immediately on initial page load")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_not_visible_immediately(self, driver):
        """Verifies ad modal is not shown at 0 seconds (delayed trigger)."""
        page = AdsPage(driver)
        page.load()

        # In the first 1-2 seconds, ad must not be visible yet
        assert not page.is_visible(page.AD_MODAL_OVERLAY, timeout=1), "Ad should not be displayed immediately upon load"

    @pytest.mark.negative
    @pytest.mark.ads
    @allure.story("Timing & State")
    @allure.title("AN-02: Ad modal does not reopen immediately after being closed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_does_not_reopen_after_dismissal(self, driver):
        """Verifies ad stays closed and does not pop up again right away."""
        page = AdsPage(driver)
        page.load()

        page.wait_for_ad_modal(timeout=10)
        page.close_ad()
        time.sleep(2)
        assert page.is_ad_closed(), "Ad modal should not reopen after being closed"

    @pytest.mark.negative
    @pytest.mark.ads
    @allure.story("Timing & State")
    @allure.title("AN-03: Close button is not interactable when ad is closed")
    @allure.severity(allure.severity_level.MINOR)
    def test_close_button_not_visible_when_ad_closed(self, driver):
        """Verifies ad close button cannot be interacted with when modal is closed."""
        page = AdsPage(driver)
        page.load()

        page.wait_for_ad_modal(timeout=10)
        page.close_ad()
        assert not page.is_visible(page.AD_CLOSE_BUTTON, timeout=2), "Close button should not be visible after closing"
