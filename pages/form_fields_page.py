import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class FormFieldsPage(BasePage):
    """Page Object for the Form Fields page."""

    URL = "https://practice-automation.com/form-fields/"

    # Locators
    PAGE_HEADER = (By.TAG_NAME, "h1")
    FORM = (By.ID, "feedbackForm")
    NAME_INPUT = (By.ID, "name-input")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "form#feedbackForm input[type='password']")

    # Drink checkboxes
    DRINK_CHECKBOXES = (By.CSS_SELECTOR, "input[name='fav_drink']")
    DRINK_WATER = (By.ID, "drink1")
    DRINK_MILK = (By.ID, "drink2")
    DRINK_COFFEE = (By.ID, "drink3")
    DRINK_WINE = (By.ID, "drink4")
    DRINK_CTRL_ALT_DELIGHT = (By.ID, "drink5")

    # Color radio buttons
    COLOR_RADIOS = (By.CSS_SELECTOR, "input[name='fav_color']")
    COLOR_RED = (By.ID, "color1")
    COLOR_BLUE = (By.ID, "color2")
    COLOR_YELLOW = (By.ID, "color3")
    COLOR_GREEN = (By.ID, "color4")
    COLOR_PINK = (By.ID, "color5")

    # Dropdown
    AUTOMATION_SELECT = (By.ID, "automation")

    # Automation Tools list
    AUTOMATION_TOOLS_LIST = (By.XPATH, "//label[normalize-space(text())='Automation tools']/following-sibling::ul[1]/li")

    # Email & Message
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_TEXTAREA = (By.ID, "message")

    # Submit button
    SUBMIT_BUTTON = (By.ID, "submit-btn")

    @allure.step("Open Form Fields page")
    def load(self) -> None:
        self.open(self.URL)

    @allure.step("Fill Name field: {name}")
    def enter_name(self, name: str) -> None:
        self.type_text(self.NAME_INPUT, name, clear_first=True)

    @allure.step("Get value of Name field")
    def get_name_value(self) -> str:
        return self.get_attribute(self.NAME_INPUT, "value") or ""

    @allure.step("Fill Password field")
    def enter_password(self, password: str) -> None:
        self.type_text(self.PASSWORD_INPUT, password, clear_first=True)

    @allure.step("Get value of Password field")
    def get_password_value(self) -> str:
        return self.get_attribute(self.PASSWORD_INPUT, "value") or ""

    @allure.step("Select drink checkbox: {drink_id}")
    def select_drink(self, drink_id: str) -> None:
        checkbox = self.find((By.ID, drink_id))
        if not checkbox.is_selected():
            checkbox.click()

    @allure.step("Unselect drink checkbox: {drink_id}")
    def unselect_drink(self, drink_id: str) -> None:
        checkbox = self.find((By.ID, drink_id))
        if checkbox.is_selected():
            checkbox.click()

    @allure.step("Check if drink {drink_id} is selected")
    def is_drink_selected(self, drink_id: str) -> bool:
        checkbox = self.find((By.ID, drink_id))
        return checkbox.is_selected()

    @allure.step("Select color radio button: {color_id}")
    def select_color(self, color_id: str) -> None:
        self.click((By.ID, color_id))

    @allure.step("Check if color radio {color_id} is selected")
    def is_color_selected(self, color_id: str) -> bool:
        radio = self.find((By.ID, color_id))
        return radio.is_selected()

    @allure.step("Select option '{visible_text}' in automation dropdown")
    def select_automation_option(self, visible_text: str) -> None:
        select_elem = self.find(self.AUTOMATION_SELECT)
        Select(select_elem).select_by_visible_text(visible_text)

    @allure.step("Get selected option from automation dropdown")
    def get_selected_automation_option(self) -> str:
        select_elem = self.find(self.AUTOMATION_SELECT)
        return Select(select_elem).first_selected_option.text.strip()

    @allure.step("Extract list of Automation Tools from the page using Selenium")
    def get_automation_tools_list(self) -> list[str]:
        elements = self.find_all(self.AUTOMATION_TOOLS_LIST)
        return [el.text.strip() for el in elements if el.text.strip()]

    @allure.step("Fill Email field: {email}")
    def enter_email(self, email: str) -> None:
        self.type_text(self.EMAIL_INPUT, email, clear_first=True)

    @allure.step("Get value of Email field")
    def get_email_value(self) -> str:
        return self.get_attribute(self.EMAIL_INPUT, "value") or ""

    @allure.step("Fill Message textarea with text")
    def enter_message(self, message: str) -> None:
        self.type_text(self.MESSAGE_TEXTAREA, message, clear_first=True)

    @allure.step("Fill Message field with comma-separated list of Automation Tools (Task requirement)")
    def fill_message_with_automation_tools(self) -> str:
        tools = self.get_automation_tools_list()
        tools_text = ", ".join(tools)
        self.enter_message(tools_text)
        return tools_text

    @allure.step("Get value of Message textarea")
    def get_message_value(self) -> str:
        return self.get_attribute(self.MESSAGE_TEXTAREA, "value") or ""

    @allure.step("Click Submit button")
    def submit(self) -> None:
        self.click(self.SUBMIT_BUTTON)

    @allure.step("Submit form and get alert text")
    def submit_and_get_alert_text(self, timeout: int = 5) -> str:
        self.submit()
        return self.get_alert_text(timeout=timeout)

    @allure.step("Submit form and accept alert")
    def submit_and_accept_alert(self, timeout: int = 5) -> None:
        self.submit()
        self.accept_alert(timeout=timeout)
