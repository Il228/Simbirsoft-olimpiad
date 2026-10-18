import allure
import pytest
from pages.form_fields_page import FormFieldsPage


@allure.epic("UI Automation Practice")
@allure.feature("Form Fields Page")
class TestFormFields:
    """Test suite for Form Fields page functionality."""

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Input Fields")
    @allure.title("FP-01: Enter Name and Password fields")
    @allure.severity(allure.severity_level.NORMAL)
    def test_enter_name_and_password(self, driver):
        """Verifies text entry into Name and Password fields."""
        page = FormFieldsPage(driver)
        page.load()

        page.enter_name("Tester")
        page.enter_password("Secret123!")

        assert page.get_name_value() == "Tester", "Name field should have entered value"
        assert page.get_password_value() == "Secret123!", "Password field should have entered value"

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Checkboxes")
    @allure.title("FP-02: Select single favorite drink checkbox")
    @allure.severity(allure.severity_level.NORMAL)
    def test_select_single_drink(self, driver):
        """Verifies selecting a single drink checkbox."""
        page = FormFieldsPage(driver)
        page.load()

        page.select_drink("drink3")  # Coffee
        assert page.is_drink_selected("drink3"), "Coffee checkbox should be selected"
        assert not page.is_drink_selected("drink1"), "Water checkbox should remain unselected"

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Checkboxes")
    @allure.title("FP-03: Select multiple favorite drink checkboxes simultaneously")
    @allure.severity(allure.severity_level.NORMAL)
    def test_select_multiple_drinks(self, driver):
        """Verifies multiple checkboxes can be selected at the same time."""
        page = FormFieldsPage(driver)
        page.load()

        page.select_drink("drink1")  # Water
        page.select_drink("drink2")  # Milk
        page.select_drink("drink5")  # Ctrl-Alt-Delight

        assert page.is_drink_selected("drink1"), "Water should be selected"
        assert page.is_drink_selected("drink2"), "Milk should be selected"
        assert page.is_drink_selected("drink5"), "Ctrl-Alt-Delight should be selected"

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Radio Buttons")
    @allure.title("FP-04: Select favorite color radio button")
    @allure.severity(allure.severity_level.NORMAL)
    def test_select_color_radio(self, driver):
        """Verifies selecting a radio button."""
        page = FormFieldsPage(driver)
        page.load()

        page.select_color("color1")  # Red
        assert page.is_color_selected("color1"), "Red color radio button should be selected"

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Radio Buttons")
    @allure.title("FP-05: Radio buttons maintain mutual exclusivity")
    @allure.severity(allure.severity_level.NORMAL)
    def test_color_radio_mutual_exclusion(self, driver):
        """Verifies that selecting another radio button deselects the previous one."""
        page = FormFieldsPage(driver)
        page.load()

        page.select_color("color2")  # Blue
        assert page.is_color_selected("color2")

        page.select_color("color4")  # Green
        assert page.is_color_selected("color4"), "Green should be selected"
        assert not page.is_color_selected("color2"), "Blue should be deselected when Green is chosen"

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Dropdown Selection")
    @allure.title("FP-06: Select options in 'Do you like automation?' dropdown")
    @allure.severity(allure.severity_level.NORMAL)
    def test_automation_dropdown_options(self, driver):
        """Verifies selecting different options from the automation select dropdown."""
        page = FormFieldsPage(driver)
        page.load()

        for option in ["Yes", "No", "Undecided"]:
            page.select_automation_option(option)
            assert page.get_selected_automation_option() == option, f"Selected option should be '{option}'"

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Data Extraction")
    @allure.title("FP-07: Extract Automation Tools list using Selenium")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_extract_automation_tools_list(self, driver):
        """Verifies extracting the list of automation tools using Selenium locators."""
        page = FormFieldsPage(driver)
        page.load()

        tools = page.get_automation_tools_list()
        expected_tools = ["Selenium", "Playwright", "Cypress", "Appium", "Katalon Studio"]

        assert len(tools) == 5, f"Expected 5 automation tools, got {len(tools)}"
        assert tools == expected_tools, f"Extracted tools {tools} do not match expected {expected_tools}"

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Requirement #5 - Fill Message with Automation Tools")
    @allure.title("FP-08: Fill Message field with comma-separated list of Automation Tools")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_fill_message_with_comma_separated_tools(self, driver):
        """Fulfills Requirement #5: extracts Automation Tools using Selenium, converts to comma-separated text, and fills Message field."""
        page = FormFieldsPage(driver)
        page.load()

        filled_text = page.fill_message_with_automation_tools()
        actual_message_value = page.get_message_value()

        expected_text = "Selenium, Playwright, Cypress, Appium, Katalon Studio"
        assert actual_message_value == expected_text, (
            f"Message textarea value '{actual_message_value}' does not match expected '{expected_text}'"
        )
        assert filled_text == expected_text

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Form Submission")
    @allure.title("FP-09: Complete entire form and submit, verify alert 'Message received!'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_form_submission_alert(self, driver):
        """Verifies filling complete form and checking JavaScript alert popup upon submission."""
        page = FormFieldsPage(driver)
        page.load()

        page.enter_name("QA Engineer")
        page.enter_password("P@ssw0rd123")
        page.select_drink("drink1")
        page.select_color("color2")
        page.select_automation_option("Yes")
        page.fill_message_with_automation_tools()
        page.enter_email("qa@example.com")

        alert_text = page.submit_and_get_alert_text()
        assert alert_text == "Message received!", f"Alert text should be 'Message received!', got '{alert_text}'"
        page.accept_alert()

    @pytest.mark.positive
    @pytest.mark.form_fields
    @allure.story("Form Reset")
    @allure.title("FP-10: Form fields are cleared/reset after alert is accepted")
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_fields_reset_after_submit(self, driver):
        """Verifies form fields reset to initial empty state following alert acceptance."""
        page = FormFieldsPage(driver)
        page.load()

        page.enter_name("Test User")
        page.select_drink("drink1")
        page.submit_and_accept_alert()

        assert page.get_name_value() == "", "Name field should be reset"
        assert not page.is_drink_selected("drink1"), "Drink checkbox should be unchecked after reset"

    # ================= NEGATIVE TESTS =================

    @pytest.mark.negative
    @pytest.mark.form_fields
    @allure.story("Validation")
    @allure.title("FN-01: Submit form without required Name field triggers HTML5 validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_without_required_name(self, driver):
        """Verifies submitting form without mandatory Name prevents JS alert from popping up."""
        page = FormFieldsPage(driver)
        page.load()

        # Name is left blank, try to submit
        page.submit()

        # Required HTML5 field prevents form submit; alert should NOT be present
        assert not page.is_visible((page.SUBMIT_BUTTON[0], page.SUBMIT_BUTTON[1] + ":disabled"), timeout=1)
        name_input = page.find(page.NAME_INPUT)
        validation_message = driver.execute_script("return arguments[0].validationMessage;", name_input)
        assert len(validation_message) > 0, "HTML5 required validation message should be present"

    @pytest.mark.negative
    @pytest.mark.form_fields
    @allure.story("Interaction")
    @allure.title("FN-02: Unselect previously checked drink checkbox")
    @allure.severity(allure.severity_level.NORMAL)
    def test_unselect_drink_checkbox(self, driver):
        """Verifies unchecking a checkbox removes its selected state."""
        page = FormFieldsPage(driver)
        page.load()

        page.select_drink("drink3")
        assert page.is_drink_selected("drink3")

        page.unselect_drink("drink3")
        assert not page.is_drink_selected("drink3"), "Checkbox should become unselected after second click"

    @pytest.mark.negative
    @pytest.mark.form_fields
    @allure.story("Validation")
    @allure.title("FN-03: Completely empty form cannot be submitted")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_completely_empty_form(self, driver):
        """Verifies submitting empty form is blocked by required fields."""
        page = FormFieldsPage(driver)
        page.load()

        page.submit()
        name_input = page.find(page.NAME_INPUT)
        is_valid = driver.execute_script("return arguments[0].checkValidity();", name_input)
        assert not is_valid, "Empty required Name field must be invalid according to HTML5 validation"

    @pytest.mark.negative
    @pytest.mark.form_fields
    @allure.story("Field Constraints")
    @allure.title("FN-04: Default dropdown option has empty/placeholder value")
    @allure.severity(allure.severity_level.MINOR)
    def test_dropdown_default_option(self, driver):
        """Verifies initial state of automation dropdown has default/empty value."""
        page = FormFieldsPage(driver)
        page.load()

        default_text = page.get_selected_automation_option()
        assert default_text == "", f"Initial dropdown selection should be blank, got '{default_text}'"
