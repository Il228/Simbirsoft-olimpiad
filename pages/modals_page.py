import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class ModalsPage(BasePage):
    """Page Object for the Modals page."""

    URL = "https://practice-automation.com/modals/"

    # Trigger buttons
    SIMPLE_MODAL_BUTTON = (By.ID, "simpleModal")
    FORM_MODAL_BUTTON = (By.ID, "formModal")

    # Simple Modal (#pum-1318)
    SIMPLE_MODAL_OVERLAY = (By.ID, "pum-1318")
    SIMPLE_MODAL_TITLE = (By.ID, "pum_popup_title_1318")
    SIMPLE_MODAL_CONTENT = (By.CSS_SELECTOR, "#popmake-1318 .pum-content p")
    SIMPLE_MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "#pum-1318 button.pum-close")

    # Form Modal (#pum-674)
    FORM_MODAL_OVERLAY = (By.ID, "pum-674")
    FORM_MODAL_TITLE = (By.ID, "pum_popup_title_674")
    FORM_MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "#pum-674 button.pum-close")
    FORM_NAME_INPUT = (By.ID, "g1051-name")
    FORM_EMAIL_INPUT = (By.ID, "g1051-email")
    FORM_MESSAGE_INPUT = (By.ID, "contact-form-comment-g1051-message")
    FORM_SUBMIT_BUTTON = (By.CSS_SELECTOR, "#pum-674 button[type='submit']")
    FORM_SUCCESS_HEADER = (By.CSS_SELECTOR, "#pum-674 div.contact-form-submission h4")
    FORM_BACK_BUTTON = (By.CSS_SELECTOR, "#pum-674 p.go-back-message a.link")
    FORM_NAME_ERROR = (By.ID, "g1051-name-text-error")
    FORM_GENERAL_ERROR = (By.CSS_SELECTOR, "#pum-674 div.contact-form__error")

    @allure.step("Open Modals page")
    def load(self) -> None:
        self.open(self.URL)

    @allure.step("Click 'Simple Modal' button")
    def open_simple_modal(self) -> None:
        self.click(self.SIMPLE_MODAL_BUTTON)

    @allure.step("Check if Simple Modal is visible")
    def is_simple_modal_visible(self) -> bool:
        return self.is_visible(self.SIMPLE_MODAL_OVERLAY, timeout=5)

    @allure.step("Get Simple Modal title text")
    def get_simple_modal_title(self) -> str:
        return self.get_text(self.SIMPLE_MODAL_TITLE)

    @allure.step("Get Simple Modal content text")
    def get_simple_modal_content(self) -> str:
        return self.get_text(self.SIMPLE_MODAL_CONTENT)

    @allure.step("Close Simple Modal via close button (×)")
    def close_simple_modal_by_button(self) -> None:
        self.click(self.SIMPLE_MODAL_CLOSE_BUTTON)

    @allure.step("Close Simple Modal using ESC key")
    def close_modal_by_esc(self) -> None:
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)

    @allure.step("Check if Simple Modal is closed")
    def is_simple_modal_closed(self) -> bool:
        return self.is_invisible(self.SIMPLE_MODAL_OVERLAY, timeout=5)

    @allure.step("Click 'Form Modal' button")
    def open_form_modal(self) -> None:
        self.click(self.FORM_MODAL_BUTTON)

    @allure.step("Check if Form Modal is visible")
    def is_form_modal_visible(self) -> bool:
        return self.is_visible(self.FORM_MODAL_OVERLAY, timeout=5)

    @allure.step("Get Form Modal title text")
    def get_form_modal_title(self) -> str:
        return self.get_text(self.FORM_MODAL_TITLE)

    @allure.step("Fill modal form fields: name={name}, email={email}, message={message}")
    def fill_modal_form(self, name: str, email: str = "", message: str = "") -> None:
        if name is not None:
            self.type_text(self.FORM_NAME_INPUT, name, clear_first=True)
        if email:
            self.type_text(self.FORM_EMAIL_INPUT, email, clear_first=True)
        if message:
            self.type_text(self.FORM_MESSAGE_INPUT, message, clear_first=True)

    @allure.step("Submit form inside modal")
    def submit_modal_form(self) -> None:
        self.click(self.FORM_SUBMIT_BUTTON)

    @allure.step("Check if modal form success message is visible")
    def is_form_success_visible(self) -> bool:
        return self.is_visible(self.FORM_SUCCESS_HEADER, timeout=6)

    @allure.step("Get modal form success header text")
    def get_form_success_header(self) -> str:
        return self.get_text(self.FORM_SUCCESS_HEADER)

    @allure.step("Click '← Back' button in modal form")
    def click_modal_form_back(self) -> None:
        self.click(self.FORM_BACK_BUTTON)

    @allure.step("Close Form Modal via close button (×)")
    def close_form_modal_by_button(self) -> None:
        self.click(self.FORM_MODAL_CLOSE_BUTTON)

    @allure.step("Check if Form Modal is closed")
    def is_form_modal_closed(self) -> bool:
        return self.is_invisible(self.FORM_MODAL_OVERLAY, timeout=5)

    @allure.step("Check if Name validation error is visible")
    def is_name_error_visible(self) -> bool:
        return self.is_visible(self.FORM_NAME_ERROR, timeout=3) or self.is_visible(self.FORM_GENERAL_ERROR, timeout=3)
