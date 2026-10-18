import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CalendarsPage(BasePage):
    """Page Object for the Calendars page."""

    URL = "https://practice-automation.com/calendars/"

    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h1")
    DATE_INPUT = (By.ID, "g1065-1-selectorenteradate")
    DATE_LABEL = (By.CSS_SELECTOR, "label.grunion-field-label.date")
    DATE_FORMAT_HINT = (By.ID, "g1065-1-selectorenteradate-text-format")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit'].pushbutton-wide")
    SUCCESS_HEADER = (By.CSS_SELECTOR, "div.contact-form-submission h4")
    SUCCESS_SUMMARY_VALUE = (By.CSS_SELECTOR, "div.jetpack_forms_contact-form-success-summary .field-value")
    BACK_BUTTON = (By.CSS_SELECTOR, "p.go-back-message a.link")
    INPUT_ERROR = (By.ID, "g1065-1-selectorenteradate-text-error")
    FORM_ERROR = (By.CSS_SELECTOR, "div.contact-form__error")

    # jQuery UI Datepicker locators
    DATEPICKER_CONTAINER = (By.ID, "ui-datepicker-div")
    DATEPICKER_DAYS = (By.CSS_SELECTOR, "#ui-datepicker-div td:not(.ui-datepicker-unselectable) a")
    DATEPICKER_NEXT = (By.CSS_SELECTOR, "#ui-datepicker-div .ui-datepicker-next")
    DATEPICKER_PREV = (By.CSS_SELECTOR, "#ui-datepicker-div .ui-datepicker-prev")
    DATEPICKER_MONTH = (By.CSS_SELECTOR, "#ui-datepicker-div .ui-datepicker-month")
    DATEPICKER_YEAR = (By.CSS_SELECTOR, "#ui-datepicker-div .ui-datepicker-year")

    @allure.step("Open Calendars page")
    def load(self) -> None:
        self.open(self.URL)

    @allure.step("Enter date: {date_str}")
    def enter_date(self, date_str: str) -> None:
        self.type_text(self.DATE_INPUT, date_str, clear_first=True)

    @allure.step("Get value from date input")
    def get_date_input_value(self) -> str:
        return self.get_attribute(self.DATE_INPUT, "value") or ""

    @allure.step("Clear date input")
    def clear_date(self) -> None:
        element = self.find(self.DATE_INPUT)
        element.clear()

    @allure.step("Click on date input field to open datepicker")
    def click_date_input(self) -> None:
        self.click(self.DATE_INPUT)

    @allure.step("Check if datepicker widget is visible")
    def is_datepicker_visible(self) -> bool:
        return self.is_visible(self.DATEPICKER_CONTAINER, timeout=3)

    @allure.step("Select day '{day}' from datepicker calendar")
    def select_day_from_datepicker(self, day: int | str) -> None:
        self.click_date_input()
        day_str = str(day)
        day_locator = (By.XPATH, f"//div[@id='ui-datepicker-div']//td[not(contains(@class,'ui-datepicker-unselectable'))]/a[normalize-space(text())='{day_str}']")
        self.click(day_locator)

    @allure.step("Click Submit button")
    def submit(self) -> None:
        self.click(self.SUBMIT_BUTTON)

    @allure.step("Check if success confirmation is displayed")
    def is_success_displayed(self) -> bool:
        return self.is_visible(self.SUCCESS_HEADER, timeout=6)

    @allure.step("Get success confirmation header text")
    def get_success_header_text(self) -> str:
        return self.get_text(self.SUCCESS_HEADER)

    @allure.step("Get submitted date value from summary")
    def get_submitted_date_summary(self) -> str:
        if self.is_visible(self.SUCCESS_SUMMARY_VALUE, timeout=5):
            return self.get_text(self.SUCCESS_SUMMARY_VALUE)
        return ""

    @allure.step("Click '← Back' button")
    def click_back(self) -> None:
        self.click(self.BACK_BUTTON)

    @allure.step("Get format hint text")
    def get_format_hint(self) -> str:
        return self.get_text(self.DATE_FORMAT_HINT)

    @allure.step("Check if validation error is displayed")
    def is_error_displayed(self) -> bool:
        return self.is_visible(self.INPUT_ERROR, timeout=3) or self.is_visible(self.FORM_ERROR, timeout=3)
