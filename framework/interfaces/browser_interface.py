"""
BrowserInterface - Selenium WebDriver wrapper with enhanced functionality.

Provides:
- Navigation methods
- Element finding with explicit waits
- Interaction methods (click, type, select, etc.)
- Advanced wait conditions
- Screenshot capture
- JavaScript execution
- Window and frame handling
"""

import logging
import os
from datetime import datetime
from typing import List, Optional, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException
)


class BrowserInterface:
    """Selenium WebDriver wrapper with logging, screenshots, and enhanced wait mechanisms."""

    DEFAULT_EXPLICIT_WAIT = 20
    DEFAULT_SCREENSHOT_DIR = "screenshots"

    def __init__(self, driver: WebDriver, config: dict, logger: logging.Logger):
        """
        Initialize BrowserInterface.

        Args:
            driver: Selenium WebDriver instance
            config: Configuration dictionary with base URL and optional settings
            logger: Logger instance for logging operations
        """
        self.driver = driver
        self.config = config
        self.logger = logger
        self.explicit_wait = int(config.get('explicit_wait', self.DEFAULT_EXPLICIT_WAIT))
        self.screenshot_dir = config.get('screenshot_dir', self.DEFAULT_SCREENSHOT_DIR)
        self.screenshots_on_failure = config.get('screenshots_on_failure', True)

        os.makedirs(self.screenshot_dir, exist_ok=True)

    # ==================== NAVIGATION METHODS ====================

    def navigate_to(self, url: str) -> None:
        """
        Navigate to a URL.

        Args:
            url: Target URL
        """
        try:
            self.driver.get(url)
            self.logger.info(f"Navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {repr(e)}")
            self._take_screenshot("navigation_failure")
            raise

    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.logger.info("Refreshing page")
        self.driver.refresh()

    def go_back(self) -> None:
        """Navigate back in browser history."""
        self.logger.info("Navigating back")
        self.driver.back()

    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        self.logger.info("Navigating forward")
        self.driver.forward()

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            Current URL as string
        """
        url = self.driver.current_url
        self.logger.debug(f"Current URL: {url}")
        return url

    def get_page_title(self) -> str:
        """
        Get the current page title.

        Returns:
            Page title as string
        """
        title = self.driver.title
        self.logger.debug(f"Page title: {title}")
        return title

    # ==================== ELEMENT FINDING METHODS ====================

    def find_element(self, by: By, value: str, timeout: Optional[int] = None) -> WebElement:
        """
        Find a single element with explicit wait.

        Args:
            by: Locator strategy (By.ID, By.XPATH, etc.)
            value: Locator value
            timeout: Optional custom timeout (uses default if not provided)

        Returns:
            WebElement if found

        Raises:
            TimeoutException: If element not found within timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait
        self.logger.debug(f"Finding element: {by}='{value}' with timeout={timeout}s")

        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            self.logger.debug(f"Element found: {by}='{value}'")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {by}='{value}' after {timeout}s")
            self._take_screenshot("element_not_found")
            raise

    def find_elements(self, by: By, value: str, timeout: Optional[int] = None) -> List[WebElement]:
        """
        Find multiple elements with explicit wait.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout

        Returns:
            List of WebElements (empty list if none found)
        """
        timeout = timeout if timeout is not None else self.explicit_wait
        self.logger.debug(f"Finding elements: {by}='{value}' with timeout={timeout}s")

        try:
            wait = WebDriverWait(self.driver, timeout)
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            self.logger.debug(f"Found {len(elements)} elements: {by}='{value}'")
            return elements
        except TimeoutException:
            self.logger.warning(f"No elements found: {by}='{value}' after {timeout}s")
            return []

    def is_element_present(self, by: By, value: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is present in the DOM.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout (default: 5)

        Returns:
            True if element is present, False otherwise
        """
        timeout = timeout if timeout is not None else 5
        try:
            self.find_element(by, value, timeout=timeout)
            return True
        except TimeoutException:
            return False

    # ==================== INTERACTION METHODS ====================

    def click(self, by: By, value: str, timeout: Optional[int] = None) -> None:
        """
        Click an element after waiting for it to be clickable.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            self.logger.info(f"Clicked: {by}='{value}'")
        except Exception as e:
            self.logger.error(f"Failed to click {by}='{value}': {repr(e)}")
            self._take_screenshot("click_failure")
            raise

    def type(self, by: By, value: str, text: str, clear_first: bool = True, timeout: Optional[int] = None) -> None:
        """
        Enter text into an input field.

        Args:
            by: Locator strategy
            value: Locator value
            text: Text to enter
            clear_first: Clear field before typing (default: True)
            timeout: Optional custom timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            element = self.find_element(by, value, timeout=timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Typed into: {by}='{value}'")
        except Exception as e:
            self.logger.error(f"Failed to type into {by}='{value}': {repr(e)}")
            self._take_screenshot("type_failure")
            raise

    def select_by_text(self, by: By, value: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Select dropdown option by visible text.

        Args:
            by: Locator strategy
            value: Locator value
            text: Visible text of option to select
            timeout: Optional custom timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            element = self.find_element(by, value, timeout=timeout)
            select = Select(element)
            select.select_by_visible_text(text)
            self.logger.info(f"Selected '{text}' from: {by}='{value}'")
        except Exception as e:
            self.logger.error(f"Failed to select '{text}' from {by}='{value}': {repr(e)}")
            self._take_screenshot("select_failure")
            raise

    def select_by_value(self, by: By, value: str, option_value: str, timeout: Optional[int] = None) -> None:
        """
        Select dropdown option by value attribute.

        Args:
            by: Locator strategy
            value: Locator value
            option_value: Value attribute of option to select
            timeout: Optional custom timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            element = self.find_element(by, value, timeout=timeout)
            select = Select(element)
            select.select_by_value(option_value)
            self.logger.info(f"Selected value '{option_value}' from: {by}='{value}'")
        except Exception as e:
            self.logger.error(f"Failed to select value '{option_value}' from {by}='{value}': {repr(e)}")
            self._take_screenshot("select_failure")
            raise

    def get_select_options(self, by: By, value: str, timeout: Optional[int] = None) -> list:
        """
        Get all option texts from a select element.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout

        Returns:
            List of option text values
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            element = self.find_element(by, value, timeout=timeout)
            select = Select(element)
            options = [option.text for option in select.options]
            self.logger.info(f"Found {len(options)} options in: {by}='{value}'")
            return options
        except Exception as e:
            self.logger.error(f"Failed to get options from {by}='{value}': {repr(e)}")
            self._take_screenshot("get_options_failure")
            raise

    def get_text(self, by: By, value: str, timeout: Optional[int] = None) -> str:
        """
        Get text content of an element.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout

        Returns:
            Element text content
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            element = self.find_element(by, value, timeout=timeout)
            text = element.text
            self.logger.debug(f"Text from {by}='{value}': '{text}'")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from {by}='{value}': {repr(e)}")
            self._take_screenshot("get_text_failure")
            raise

    def get_attribute(self, by: By, value: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Get attribute value of an element.

        Args:
            by: Locator strategy
            value: Locator value
            attribute: Attribute name
            timeout: Optional custom timeout

        Returns:
            Attribute value or None
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            element = self.find_element(by, value, timeout=timeout)
            attr_value = element.get_attribute(attribute)
            self.logger.debug(f"Attribute '{attribute}' from {by}='{value}': '{attr_value}'")
            return attr_value
        except Exception as e:
            self.logger.error(f"Failed to get attribute '{attribute}' from {by}='{value}': {repr(e)}")
            self._take_screenshot("get_attribute_failure")
            raise

    def is_element_displayed(self, by: By, value: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible on page.

        Waits for element to be VISIBLE (not just present in DOM).

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout (default: 5)

        Returns:
            True if element is displayed, False otherwise
        """
        timeout = timeout if timeout is not None else 5
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located((by, value)))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def hover(self, by: By, value: str, timeout: Optional[int] = None) -> None:
        """
        Hover over an element using ActionChains.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait
        try:
            element = self.find_element(by, value, timeout=timeout)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.logger.debug(f"Hovered over: {by}='{value}'")
        except Exception as e:
            self.logger.error(f"Failed to hover over {by}='{value}': {repr(e)}")
            self._take_screenshot("hover_failure")
            raise

    def is_element_clickable(self, by: By, value: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is clickable (visible and enabled).

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout

        Returns:
            True if element is clickable, False otherwise
        """
        timeout = timeout if timeout is not None else self.explicit_wait
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable((by, value)))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    # ==================== ADVANCED WAIT METHODS ====================

    def wait_for_element_visible(self, by: By, value: str, timeout: Optional[int] = None) -> WebElement:
        """
        Wait for element to be visible.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout

        Returns:
            WebElement when visible

        Raises:
            TimeoutException: If element not visible within timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located((by, value)))
            self.logger.debug(f"Element visible: {by}='{value}'")
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible: {by}='{value}' after {timeout}s")
            self._take_screenshot("element_not_visible")
            raise

    def wait_for_element_invisible(self, by: By, value: str, timeout: Optional[int] = None) -> bool:
        """
        Wait for element to become invisible or not present.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout

        Returns:
            True if element becomes invisible

        Raises:
            TimeoutException: If element still visible after timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.invisibility_of_element_located((by, value)))
            self.logger.debug(f"Element invisible: {by}='{value}'")
            return True
        except TimeoutException:
            self.logger.error(f"Element still visible: {by}='{value}' after {timeout}s")
            self._take_screenshot("element_still_visible")
            raise

    def wait_for_text_in_element(self, by: By, value: str, text: str, timeout: Optional[int] = None) -> bool:
        """
        Wait for specific text to appear in element.

        Args:
            by: Locator strategy
            value: Locator value
            text: Expected text
            timeout: Optional custom timeout

        Returns:
            True if text appears in element

        Raises:
            TimeoutException: If text not present after timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.text_to_be_present_in_element((by, value), text))
            self.logger.debug(f"Text '{text}' present in: {by}='{value}'")
            return True
        except TimeoutException:
            self.logger.error(f"Text '{text}' not in {by}='{value}' after {timeout}s")
            self._take_screenshot("text_not_present")
            raise

    def wait_for_url_contains(self, url_fragment: str, timeout: Optional[int] = None) -> bool:
        """
        Wait for URL to contain specific text.

        Args:
            url_fragment: Expected URL fragment
            timeout: Optional custom timeout

        Returns:
            True if URL contains fragment

        Raises:
            TimeoutException: If URL doesn't contain fragment after timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.url_contains(url_fragment))
            self.logger.debug(f"URL contains: '{url_fragment}'")
            return True
        except TimeoutException:
            self.logger.error(f"URL does not contain '{url_fragment}' after {timeout}s")
            self._take_screenshot("url_check_failure")
            raise

    # ==================== SCREENSHOT METHODS ====================

    def take_screenshot(self, name: str) -> str:
        """
        Take a screenshot and save with timestamp.

        Args:
            name: Base name for screenshot file

        Returns:
            Path to saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        try:
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save screenshot: {repr(e)}")
            raise

    def _take_screenshot(self, name: str) -> Optional[str]:
        """
        Internal method to take screenshot on failure (if enabled).

        Args:
            name: Base name for screenshot file

        Returns:
            Path to saved screenshot or None if disabled
        """
        if self.screenshots_on_failure:
            try:
                return self.take_screenshot(name)
            except Exception:
                return None
        return None

    # ==================== JAVASCRIPT EXECUTION ====================

    def execute_script(self, script: str, *args) -> any:
        """
        Execute JavaScript code.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Script execution result
        """
        self.logger.debug(f"Executing JavaScript: {script[:100]}...")
        try:
            result = self.driver.execute_script(script, *args)
            return result
        except Exception as e:
            self.logger.error(f"Failed to execute JavaScript: {repr(e)}")
            raise

    def scroll_to_element(self, by: By, value: str, timeout: Optional[int] = None) -> None:
        """
        Scroll element into view.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout
        """
        element = self.find_element(by, value, timeout=timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.debug(f"Scrolled to: {by}='{value}'")

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self) -> None:
        """Scroll to top of page."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    # ==================== WINDOW AND FRAME HANDLING ====================

    def switch_to_frame(self, by: By, value: str, timeout: Optional[int] = None) -> None:
        """
        Switch to iframe.

        Args:
            by: Locator strategy
            value: Locator value
            timeout: Optional custom timeout
        """
        timeout = timeout if timeout is not None else self.explicit_wait

        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.frame_to_be_available_and_switch_to_it((by, value)))
            self.logger.info(f"Switched to frame: {by}='{value}'")
        except Exception as e:
            self.logger.error(f"Failed to switch to frame: {repr(e)}")
            self._take_screenshot("frame_switch_failure")
            raise

    def switch_to_default_content(self) -> None:
        """Switch back to main page content from frame."""
        self.driver.switch_to.default_content()

    def switch_to_window(self, window_handle: str) -> None:
        """
        Switch to window by handle.

        Args:
            window_handle: Window handle string
        """
        self.driver.switch_to.window(window_handle)

    def get_window_handles(self) -> List[str]:
        """
        Get all window handles.

        Returns:
            List of window handle strings
        """
        return self.driver.window_handles

    def switch_to_new_window(self) -> str:
        """
        Switch to the most recently opened window.

        Returns:
            New window handle
        """
        handles = self.get_window_handles()
        new_window = handles[-1]
        self.switch_to_window(new_window)
        return new_window

    def close_current_window(self) -> None:
        """Close the current window."""
        self.driver.close()

    # ==================== UTILITY METHODS ====================

    def get_page_source(self) -> str:
        """
        Get page source HTML.

        Returns:
            Page source as string
        """
        return self.driver.page_source
