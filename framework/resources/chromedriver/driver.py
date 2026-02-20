"""
WebDriver Factory - Creates and configures browser instances.

Handles driver initialization with appropriate options (headless, window size, etc.).
Supports Brave browser (Chromium-based) as the default browser.
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


# Brave browser executable paths by platform
BRAVE_PATHS = {
    "win32": [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
    ],
    "darwin": [
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    ],
    "linux": [
        "/usr/bin/brave-browser",
        "/usr/bin/brave",
        "/snap/bin/brave",
    ],
}


def _find_brave_binary():
    """Find Brave browser executable on the system."""
    import sys
    platform = sys.platform

    paths = BRAVE_PATHS.get(platform, [])
    for path in paths:
        if os.path.exists(path):
            return path

    return None


def create_driver(headless=False, window_size="1920x1080", browser="chrome"):
    """
    Create and configure a browser driver instance.

    Args:
        headless: Run browser in headless mode (default: False)
        window_size: Browser window size as "WIDTHxHEIGHT" (default: "1920x1080")
        browser: Browser to use - "brave" or "chrome" (default: "chrome")

    Returns:
        WebDriver: Configured browser driver instance
    """
    # Configure Chrome options (works for Brave since it's Chromium-based)
    chrome_options = Options()

    # Set Brave binary location if using Brave
    if browser.lower() == "brave":
        brave_path = _find_brave_binary()
        if brave_path:
            chrome_options.binary_location = brave_path
        else:
            raise FileNotFoundError(
                "Brave browser not found. Install Brave or use browser='chrome'"
            )

    # Headless mode
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")

    # Window size
    chrome_options.add_argument(f"--window-size={window_size}")

    # Performance and stability options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Suppress logging
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Create driver using WebDriver Manager
    # For Brave, we use ChromeType.BRAVE to get compatible chromedriver
    if browser.lower() == "brave":
        service = Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
    else:
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Set implicit wait
    driver.implicitly_wait(10)

    # Maximize window if not headless
    if not headless:
        driver.maximize_window()

    return driver
