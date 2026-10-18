import allure
import pytest
from pages.modals_page import ModalsPage


@allure.epic("UI Automation Practice")
@allure.feature("Modals Page")
class TestModals:
    """Test suite for Modals page functionality."""

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Trigger Buttons Display")
    @allure.title("MP-01: Verify modal trigger buttons are visible on page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_buttons_visible(self, driver):
        """Verifies both Simple Modal and Form Modal buttons are present."""
        page = ModalsPage(driver)
        page.load()

        assert page.is_visible(page.SIMPLE_MODAL_BUTTON), "Simple Modal button should be visible"
        assert page.is_visible(page.FORM_MODAL_BUTTON), "Form Modal button should be visible"

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Simple Modal")
    @allure.title("MP-02: Open Simple Modal successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_simple_modal(self, driver):
        """Verifies clicking Simple Modal button displays the modal."""
        page = ModalsPage(driver)
        page.load()

        page.open_simple_modal()
        assert page.is_simple_modal_visible(), "Simple modal should appear after clicking trigger button"

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Simple Modal")
    @allure.title("MP-03: Verify Simple Modal title and text content")
    @allure.severity(allure.severity_level.NORMAL)
    def test_simple_modal_content(self, driver):
        """Verifies text within Simple Modal matches expected values."""
        page = ModalsPage(driver)
        page.load()

        page.open_simple_modal()
        assert page.get_simple_modal_title() == "Simple Modal", "Modal title should be 'Simple Modal'"
        assert "Hi, I’m a simple modal." in page.get_simple_modal_content(), "Modal content should match expected text"

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Simple Modal")
    @allure.title("MP-04: Close Simple Modal using close button (×)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_close_simple_modal_by_button(self, driver):
        """Verifies clicking × closes the Simple Modal."""
        page = ModalsPage(driver)
        page.load()

        page.open_simple_modal()
        assert page.is_simple_modal_visible()

        page.close_simple_modal_by_button()
        assert page.is_simple_modal_closed(), "Simple modal should be closed after clicking close button"

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Simple Modal")
    @allure.title("MP-05: Close Simple Modal using Escape key")
    @allure.severity(allure.severity_level.NORMAL)
    def test_close_simple_modal_by_esc(self, driver):
        """Verifies pressing ESC closes the Simple Modal."""
        page = ModalsPage(driver)
        page.load()

        page.open_simple_modal()
        assert page.is_simple_modal_visible()

        page.close_modal_by_esc()
        assert page.is_simple_modal_closed(), "Simple modal should close when ESC is pressed"

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Form Modal")
    @allure.title("MP-06: Open Form Modal successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_form_modal(self, driver):
        """Verifies clicking Form Modal button displays the modal."""
        page = ModalsPage(driver)
        page.load()

        page.open_form_modal()
        assert page.is_form_modal_visible(), "Form modal should appear after clicking trigger button"

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Form Modal")
    @allure.title("MP-07: Verify Form Modal title")
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_modal_title(self, driver):
        """Verifies Form Modal has expected title."""
        page = ModalsPage(driver)
        page.load()

        page.open_form_modal()
        assert page.get_form_modal_title() == "Modal Containing A Form"

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Form Modal")
    @allure.title("MP-08: Submit Form Modal with valid required and optional data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_form_modal_valid_data(self, driver):
        """Verifies submitting form with Name, Email, and Message displays success."""
        page = ModalsPage(driver)
        page.load()

        page.open_form_modal()
        page.fill_modal_form(name="John Doe", email="john.doe@example.com", message="Testing modal form")
        page.submit_modal_form()

        assert page.is_form_success_visible(), "Success message should be displayed upon valid submission"
        assert "Thank you for your response" in page.get_form_success_header()

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Form Modal")
    @allure.title("MP-09: Click '← Back' button after Form Modal submission")
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_modal_back_button(self, driver):
        """Verifies clicking Back returns to form inputs inside modal."""
        page = ModalsPage(driver)
        page.load()

        page.open_form_modal()
        page.fill_modal_form(name="Alice", email="alice@test.com", message="Hello")
        page.submit_modal_form()
        assert page.is_form_success_visible()

        page.click_modal_form_back()
        assert page.is_visible(page.FORM_NAME_INPUT), "Name input should be visible again after clicking Back"

    @pytest.mark.positive
    @pytest.mark.modals
    @allure.story("Form Modal")
    @allure.title("MP-10: Close Form Modal using close button (×)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_close_form_modal_by_button(self, driver):
        """Verifies clicking × closes the Form Modal."""
        page = ModalsPage(driver)
        page.load()

        page.open_form_modal()
        assert page.is_form_modal_visible()

        page.close_form_modal_by_button()
        assert page.is_form_modal_closed(), "Form modal should close after clicking close button"

    # ================= NEGATIVE TESTS =================

    @pytest.mark.negative
    @pytest.mark.modals
    @allure.story("Form Modal Validation")
    @allure.title("MN-01: Submit Form Modal without required Name field")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_modal_without_name(self, driver):
        """Verifies submitting form without mandatory Name prevents success confirmation."""
        page = ModalsPage(driver)
        page.load()

        page.open_form_modal()
        page.fill_modal_form(name="", email="test@example.com", message="No name provided")
        page.submit_modal_form()

        assert not page.is_form_success_visible(), "Form should not be submitted without required Name"

    @pytest.mark.negative
    @pytest.mark.modals
    @allure.story("Form Modal Validation")
    @allure.title("MN-02: Submit Form Modal with whitespace-only in Name field")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_modal_name_whitespace(self, driver):
        """Verifies whitespace-only Name does not pass validation."""
        page = ModalsPage(driver)
        page.load()

        page.open_form_modal()
        page.fill_modal_form(name="     ", email="valid@example.com", message="Whitespace name")
        page.submit_modal_form()

        assert not page.is_form_success_visible(), "Form should reject whitespace-only Name"

    @pytest.mark.negative
    @pytest.mark.modals
    @allure.story("Form Modal Validation")
    @allure.title("MN-03: Submit Form Modal with invalid email format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_modal_invalid_email(self, driver):
        """Verifies invalid email format prevents submission or triggers validation."""
        page = ModalsPage(driver)
        page.load()

        page.open_form_modal()
        page.fill_modal_form(name="Bob", email="invalid-email-format", message="Bad email")
        page.submit_modal_form()

        assert not page.is_form_success_visible(), "Form must not submit successfully with invalid email address"

    @pytest.mark.negative
    @pytest.mark.modals
    @allure.story("Modal Overlay")
    @allure.title("MN-04: Modal overlay is active when modal is open")
    @allure.severity(allure.severity_level.MINOR)
    def test_modal_overlay_active(self, driver):
        """Verifies modal overlay exists and covers the screen when modal is opened."""
        page = ModalsPage(driver)
        page.load()

        page.open_simple_modal()
        assert page.is_visible(page.SIMPLE_MODAL_OVERLAY), "Modal overlay should be visible and active"
