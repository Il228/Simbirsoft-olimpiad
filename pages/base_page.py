import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class BasePage:
    """Base class for all Page Objects containing common Selenium interactions and explicit waits."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout

    @allure.step("Open URL: {url}")
    def open(self, url: str) -> None:
        """Navigates to the specified URL."""
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Returns the current browser URL."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Returns page title."""
        return self.driver.title

    def find(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        """Waits for and returns an element present on the page."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        """Waits for and returns a visible element."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: tuple[str, str], timeout: int | None = None) -> list[WebElement]:
        """Returns all elements matching the locator."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def click(self, locator: tuple[str, str], timeout: int | None = None) -> None:
        """Waits for an element to be clickable and performs a click, with JS click fallback if intercepted."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator))
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
            wait.until(EC.element_to_be_clickable(locator)).click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator: tuple[str, str], text: str, clear_first: bool = True, timeout: int | None = None) -> None:
        """Types text into an input field, optionally clearing it first."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
        element = wait.until(EC.visibility_of_element_located(locator))
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[str, str], timeout: int | None = None) -> str:
        """Returns visible text of the element."""
        element = self.find_visible(locator, timeout=timeout)
        return element.text.strip()

    def get_attribute(self, locator: tuple[str, str], attribute: str, timeout: int | None = None) -> str | None:
        """Returns the requested attribute value of an element."""
        element = self.find(locator, timeout=timeout)
        return element.get_attribute(attribute)

    def is_visible(self, locator: tuple[str, str], timeout: int = 3) -> bool:
        """Checks if an element is visible on the page within given timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_invisible(self, locator: tuple[str, str], timeout: int = 5) -> bool:
        """Waits until an element becomes invisible or not present."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            return False

    def scroll_to_element(self, locator: tuple[str, str]) -> None:
        """Scrolls the page until the element is brought into view."""
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def get_alert_text(self, timeout: int = 5) -> str:
        """Waits for alert and returns its text."""
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        return alert.text

    def accept_alert(self, timeout: int = 5) -> None:
        """Waits for alert and accepts it."""
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert.accept()

    def dismiss_alert(self, timeout: int = 5) -> None:
        """Waits for alert and dismisses it."""
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert.dismiss()
