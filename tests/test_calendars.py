import allure
import pytest
from datetime import date
from pages.calendars_page import CalendarsPage


@allure.epic("UI Automation Practice")
@allure.feature("Calendars Page")
class TestCalendars:
    """Test suite for Calendars page functionality."""

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Page Elements Display")
    @allure.title("CP-01: Verify all key elements are visible on Calendars page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_calendars_page_elements_displayed(self, driver):
        """Verifies date input, label, format hint, and submit button are present."""
        page = CalendarsPage(driver)
        page.load()

        assert page.is_visible(page.DATE_INPUT), "Date input field should be visible"
        assert page.is_visible(page.DATE_LABEL), "Date label should be visible"
        assert page.is_visible(page.DATE_FORMAT_HINT), "Date format hint (YYYY-MM-DD) should be visible"
        assert page.is_visible(page.SUBMIT_BUTTON), "Submit button should be visible"
        assert "YYYY-MM-DD" in page.get_format_hint(), "Format hint should indicate YYYY-MM-DD"

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Date Input")
    @allure.title("CP-02: Enter date directly into input field")
    @allure.severity(allure.severity_level.NORMAL)
    def test_enter_date_directly(self, driver):
        """Verifies entering date as text properly updates input field value."""
        page = CalendarsPage(driver)
        page.load()

        test_date = "2026-10-18"
        page.enter_date(test_date)
        assert page.get_date_input_value() == test_date, f"Input value should match entered date {test_date}"

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Form Submission")
    @allure.title("CP-03: Submit form with today's date successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_today_date(self, driver):
        """Verifies submitting form with current date displays success message."""
        page = CalendarsPage(driver)
        page.load()

        today_str = date.today().strftime("%Y-%m-%d")
        page.enter_date(today_str)
        page.submit()

        assert page.is_success_displayed(), "Success message should be displayed after valid submission"
        assert "Thank you for your response" in page.get_success_header_text()

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Form Submission")
    @allure.title("CP-04: Submit form with future date")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_future_date(self, driver):
        """Verifies valid future date can be submitted successfully."""
        page = CalendarsPage(driver)
        page.load()

        future_date = "2027-06-15"
        page.enter_date(future_date)
        page.submit()

        assert page.is_success_displayed(), "Success message should appear for future date submission"

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Form Submission")
    @allure.title("CP-05: Submit form with past date")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_past_date(self, driver):
        """Verifies valid past date can be submitted successfully."""
        page = CalendarsPage(driver)
        page.load()

        past_date = "2021-01-01"
        page.enter_date(past_date)
        page.submit()

        assert page.is_success_displayed(), "Success message should appear for past date submission"

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Datepicker Widget")
    @allure.title("CP-06: Datepicker widget opens when clicking date input field")
    @allure.severity(allure.severity_level.NORMAL)
    def test_open_datepicker_widget(self, driver):
        """Verifies jQuery UI calendar popup opens upon clicking the input."""
        page = CalendarsPage(driver)
        page.load()

        page.click_date_input()
        assert page.is_datepicker_visible(), "Calendar widget should become visible when input is clicked"

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Datepicker Widget")
    @allure.title("CP-07: Select a day using Datepicker widget")
    @allure.severity(allure.severity_level.NORMAL)
    def test_select_day_from_datepicker(self, driver):
        """Verifies clicking a day in datepicker populates the input field."""
        page = CalendarsPage(driver)
        page.load()

        page.select_day_from_datepicker(15)
        entered_val = page.get_date_input_value()
        assert len(entered_val) > 0, "Input should have a value after datepicker selection"
        assert entered_val.endswith("15"), f"Selected date '{entered_val}' should end with selected day 15"

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Form Submission")
    @allure.title("CP-08: Submit date selected from Datepicker widget")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_datepicker_selected_date(self, driver):
        """Verifies submission after picking a date from the calendar widget."""
        page = CalendarsPage(driver)
        page.load()

        page.select_day_from_datepicker(10)
        page.submit()
        assert page.is_success_displayed(), "Form should submit successfully with date selected from widget"

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Navigation")
    @allure.title("CP-09: Click '← Back' button after submission returns to form")
    @allure.severity(allure.severity_level.NORMAL)
    def test_back_button_navigation(self, driver):
        """Verifies clicking ← Back after submission returns user to the form."""
        page = CalendarsPage(driver)
        page.load()

        page.enter_date("2026-10-18")
        page.submit()
        assert page.is_success_displayed(), "Success message should be displayed"

        page.click_back()
        assert page.is_visible(page.DATE_INPUT), "Date input should be visible again after clicking Back"

    @pytest.mark.positive
    @pytest.mark.calendars
    @allure.story("Date Input")
    @allure.title("CP-10: Clear and re-enter date in input field")
    @allure.severity(allure.severity_level.MINOR)
    def test_clear_and_reenter_date(self, driver):
        """Verifies that date can be cleared and replaced with a new date value."""
        page = CalendarsPage(driver)
        page.load()

        page.enter_date("2025-01-01")
        assert page.get_date_input_value() == "2025-01-01"

        page.clear_date()
        assert page.get_date_input_value() == ""

        page.enter_date("2026-12-31")
        assert page.get_date_input_value() == "2026-12-31"

    # ================= NEGATIVE TESTS =================

    @pytest.mark.negative
    @pytest.mark.calendars
    @allure.story("Validation")
    @allure.title("CN-01: Submit empty date field")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_empty_date(self, driver):
        """Verifies submitting with empty date triggers error or prevents success message."""
        page = CalendarsPage(driver)
        page.load()

        page.clear_date()
        page.submit()

        assert not page.is_success_displayed(), "Success message must not be shown when submitting empty date"

    @pytest.mark.negative
    @pytest.mark.calendars
    @allure.story("Validation")
    @allure.title("CN-02: Submit invalid text characters instead of date")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_letters_as_date(self, driver):
        """Verifies non-date text submission does not result in successful submission."""
        page = CalendarsPage(driver)
        page.load()

        page.enter_date("not-a-valid-date")
        page.submit()

        assert not page.is_success_displayed(), "Form should reject alphabetic text instead of date"

    @pytest.mark.negative
    @pytest.mark.calendars
    @allure.story("Validation")
    @allure.title("CN-03: Submit date in wrong format (DD/MM/YYYY instead of YYYY-MM-DD)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_wrong_date_format(self, driver):
        """Verifies format other than YYYY-MM-DD does not result in successful submission."""
        page = CalendarsPage(driver)
        page.load()

        page.enter_date("31/12/2026")
        page.submit()

        assert not page.is_success_displayed(), "Form must not accept DD/MM/YYYY format"

    @pytest.mark.negative
    @pytest.mark.calendars
    @allure.story("Validation")
    @allure.title("CN-04: Submit whitespace-only in date field")
    @allure.severity(allure.severity_level.MINOR)
    def test_submit_spaces_in_date(self, driver):
        """Verifies whitespace input does not pass date validation."""
        page = CalendarsPage(driver)
        page.load()

        page.enter_date("     ")
        page.submit()

        assert not page.is_success_displayed(), "Form must not submit with only spaces in date"
