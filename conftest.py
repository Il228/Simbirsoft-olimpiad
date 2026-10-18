import os
import shutil
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def is_chrome_installed() -> bool:
    """Checks whether Google Chrome binary exists locally on Windows."""
    standard_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    if shutil.which("chrome") or shutil.which("google-chrome"):
        return True
    return any(os.path.isfile(p) for p in standard_paths)


def is_edge_installed() -> bool:
    """Checks whether Microsoft Edge binary exists locally on Windows."""
    standard_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    if shutil.which("msedge") or shutil.which("edge"):
        return True
    return any(os.path.isfile(p) for p in standard_paths)


def pytest_addoption(parser):
    """Adds CLI options for pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default="auto",
        help="Browser to run tests: chrome, edge, firefox, auto (default: auto)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)"
    )
    parser.addoption(
        "--no-headless",
        action="store_false",
        dest="headless",
        help="Run browser with visible UI (headful mode)"
    )


@pytest.fixture(scope="function")
def driver(request):
    """Initializes and returns a Selenium WebDriver instance for each test."""
    browser_name = request.config.getoption("--browser").lower()
    is_headless = request.config.getoption("--headless")

    driver_instance = None

    def get_chrome():
        opts = ChromeOptions()
        if is_headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=opts)

    def get_edge():
        opts = EdgeOptions()
        if is_headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        return webdriver.Edge(options=opts)

    def get_firefox():
        opts = FirefoxOptions()
        if is_headless:
            opts.add_argument("-headless")
        opts.add_argument("--width=1920")
        opts.add_argument("--height=1080")
        return webdriver.Firefox(options=opts)

    # Resolution logic
    if browser_name == "auto":
        if is_chrome_installed():
            driver_instance = get_chrome()
        elif is_edge_installed():
            driver_instance = get_edge()
        else:
            driver_instance = get_firefox()
    elif browser_name == "chrome":
        if is_chrome_installed():
            driver_instance = get_chrome()
        else:
            # Fallback to local Chromium (Edge) if Chrome is not installed
            driver_instance = get_edge()
    elif browser_name == "edge":
        driver_instance = get_edge()
    elif browser_name == "firefox":
        driver_instance = get_firefox()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}. Supported: chrome, edge, firefox, auto.")

    driver_instance.set_page_load_timeout(30)
    driver_instance.maximize_window()

    yield driver_instance

    driver_instance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to capture screenshots and attach to Allure report upon test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                screenshot_png = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot_png,
                    name=f"Failure_Screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    driver.page_source,
                    name=f"Page_Source_{item.name}",
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception as e:
                print(f"Failed to capture failure screenshot: {e}")
