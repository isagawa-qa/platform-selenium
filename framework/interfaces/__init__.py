"""
Framework interfaces module.

Exports:
- BrowserInterface: Selenium WebDriver wrapper
- CliInterface: subprocess + pexpect CLI driver
"""

from .browser_interface import BrowserInterface
from .cli_interface import CliInterface

__all__ = ['BrowserInterface', 'CliInterface']
