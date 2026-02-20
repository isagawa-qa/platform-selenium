"""
Pytest configuration and fixtures.

Provides reusable fixtures for test execution:
- driver: Browser driver instance with headless option
- config: Environment configuration (base URL)
- test_users: Test user credentials
- browser: BrowserInterface wrapper with all dependencies
"""

import ast
import os
import sys
import json
import logging
import pytest
from pathlib import Path
from datetime import datetime

# Project root and framework path
PROJECT_ROOT = Path(__file__).parent.parent
FRAMEWORK_PATH = str(PROJECT_ROOT / "framework")
sys.path.insert(0, FRAMEWORK_PATH)

from resources.chromedriver.driver import create_driver
from interfaces.browser_interface import BrowserInterface

logger = logging.getLogger("BrowserInterface")


# ------------------------------------------------------------------------------
# Command line options
# ------------------------------------------------------------------------------

def pytest_addoption(parser):
    """
    Configure custom command line options for running tests.

    Falls back to environment variables (.env) when CLI flags are not provided.
    """
    parser.addoption("--env", action="store",
                     default=os.environ.get("TEST_ENV", "DEFAULT"),
                     help="Environment to test against (default: DEFAULT)")
    parser.addoption("--headless", action="store_true",
                     default=os.environ.get("HEADLESS", "false").strip().lower() == "true",
                     help="Run browser in headless mode")
    parser.addoption("--browser", action="store",
                     default=os.environ.get("BROWSER", "chrome"),
                     help="Browser to use: chrome or brave (default: chrome)")


# ------------------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def driver(request):
    """
    Create and teardown browser driver for each test.

    Function-scoped: New driver instance per test.
    Supports Chrome and Brave via --browser flag.
    """
    headless = request.config.getoption("--headless")
    browser_type = request.config.getoption("--browser")

    chromedriver = create_driver(headless=headless, browser=browser_type)
    try:
        yield chromedriver
    finally:
        chromedriver.quit()


@pytest.fixture(scope="session")
def config(request):
    """
    Load environment configuration.

    Session-scoped: Loaded once per test session.
    """
    env_id = request.config.getoption("--env")

    config_path = PROJECT_ROOT / "framework" / "resources" / "config" / "environment_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        environments = json.load(f)

    if env_id not in environments:
        raise ValueError(f"No environment match found for environment ID: {env_id}")

    yield environments[env_id]


@pytest.fixture(scope="session")
def test_users():
    """
    Load test user credentials.

    Session-scoped: Loaded once per test session.
    """
    users_path = PROJECT_ROOT / "tests" / "data" / "test_users.json"
    with open(users_path, "r", encoding="utf-8") as f:
        yield json.load(f)


@pytest.fixture
def browser(driver, config):
    """
    Create BrowserInterface wrapper with driver, config, and logger.

    Function-scoped: New instance per test.
    """
    yield BrowserInterface(driver, config, logger)


# ==============================================================================
# HTML REPORT ENHANCEMENTS
# ==============================================================================
def pytest_html_report_title(report):
    """Customize HTML report title."""
    report.title = "Isagawa QA Platform - Test Report"


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """Add custom metadata to report header and auto-register markers."""
    env_id = config.getoption("--env")
    browser_type = config.getoption("--browser")

    # Load base URL from environment config
    config_path = PROJECT_ROOT / "framework" / "resources" / "config" / "environment_config.json"
    base_url = ""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            environments = json.load(f)
        base_url = environments.get(env_id, {}).get("url", "")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    config._metadata = {
        'Project': 'Isagawa QA Platform',
        'Environment': env_id,
        'Base URL': base_url,
        'Browser': browser_type.capitalize(),
        'Headless Mode': config.getoption('--headless'),
        'Report Generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Dynamic marker registration - scans test files for @pytest.mark.X
    _register_dynamic_markers(config)


def _register_dynamic_markers(config):
    """
    Scan test files and auto-register any pytest markers found.

    Allows AI-generated tests to use custom markers without manual pytest.ini updates.
    """
    markers = set()
    tests_dir = PROJECT_ROOT / "tests"

    for test_file in tests_dir.rglob("*.py"):
        try:
            tree = ast.parse(test_file.read_text(encoding="utf-8"))

            for node in ast.walk(tree):
                if (isinstance(node, ast.Attribute) and
                    isinstance(node.value, ast.Attribute) and
                    node.value.attr == "mark" and
                    isinstance(node.value.value, ast.Name) and
                    node.value.value.id == "pytest"):
                    markers.add(node.attr)
        except (SyntaxError, UnicodeDecodeError):
            pass

    for marker in markers:
        config.addinivalue_line("markers", f"{marker}: Auto-discovered marker")
