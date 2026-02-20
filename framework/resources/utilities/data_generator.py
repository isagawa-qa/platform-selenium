"""
Test data generation utility using Faker and JSON data loading.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from faker import Faker


class DataGenerator:
    """Test data generator using Faker library and JSON data files."""

    def __init__(self, locale: str = 'en_US', data_dir: str = 'framework/resources/data'):
        """
        Initialize DataGenerator.

        Args:
            locale: Faker locale (default: en_US)
            data_dir: Directory containing JSON data files
        """
        self.faker = Faker(locale)
        self.data_dir = data_dir
        Faker.seed(0)  # Set seed for reproducibility in tests

    # ==================== PERSONAL DATA ====================

    def generate_first_name(self) -> str:
        """Generate random first name."""
        return self.faker.first_name()

    def generate_last_name(self) -> str:
        """Generate random last name."""
        return self.faker.last_name()

    def generate_full_name(self) -> str:
        """Generate random full name."""
        return self.faker.name()

    def generate_email(self, prefix: Optional[str] = None) -> str:
        """
        Generate random email address.

        Args:
            prefix: Optional prefix for email (e.g., 'test_user')

        Returns:
            Email address string
        """
        if prefix:
            domain = self.faker.free_email_domain()
            return f"{prefix}_{self.faker.random_number(digits=6)}@{domain}"
        return self.faker.email()

    def generate_phone_number(self) -> str:
        """Generate random phone number."""
        return self.faker.phone_number()

    def generate_password(self, length: int = 12, special_chars: bool = True) -> str:
        """
        Generate random password.

        Args:
            length: Password length
            special_chars: Include special characters

        Returns:
            Password string
        """
        return self.faker.password(
            length=length,
            special_chars=special_chars,
            digits=True,
            upper_case=True,
            lower_case=True
        )

    # ==================== ADDRESS DATA ====================

    def generate_address_line(self) -> str:
        """Generate random street address."""
        return self.faker.street_address()

    def generate_city(self) -> str:
        """Generate random city name."""
        return self.faker.city()

    def generate_state(self) -> str:
        """Generate random state name."""
        return self.faker.state()

    def generate_state_abbr(self) -> str:
        """Generate random state abbreviation."""
        return self.faker.state_abbr()

    def generate_zipcode(self) -> str:
        """Generate random zip code."""
        return self.faker.zipcode()

    def generate_country(self) -> str:
        """Generate random country name."""
        return self.faker.country()

    def generate_full_address(self) -> Dict[str, str]:
        """
        Generate complete address dictionary.

        Returns:
            Dictionary with address components
        """
        return {
            'address1': self.generate_address_line(),
            'address2': self.faker.secondary_address() if self.faker.boolean(chance_of_getting_true=30) else '',
            'city': self.generate_city(),
            'state': self.generate_state(),
            'zipcode': self.generate_zipcode(),
            'country': 'United States'  # Default to US for test site
        }

    # ==================== COMPANY DATA ====================

    def generate_company_name(self) -> str:
        """Generate random company name."""
        return self.faker.company()

    # ==================== PAYMENT DATA ====================

    def generate_credit_card_number(self, card_type: Optional[str] = None) -> str:
        """
        Generate random credit card number.

        Args:
            card_type: Card type (visa, mastercard, amex, etc.)

        Returns:
            Credit card number
        """
        return self.faker.credit_card_number(card_type=card_type)

    def generate_credit_card_cvv(self) -> str:
        """Generate random CVV code."""
        return self.faker.credit_card_security_code()

    def generate_credit_card_expire(self) -> str:
        """Generate random credit card expiration date."""
        return self.faker.credit_card_expire()

    # ==================== USER DATA GENERATION ====================

    def generate_user_data(self, user_type: str = 'customer') -> Dict[str, Any]:
        """
        Generate complete user data for registration.

        Args:
            user_type: Type of user (customer, admin, etc.)

        Returns:
            Dictionary with complete user data
        """
        first_name = self.generate_first_name()
        last_name = self.generate_last_name()
        email = self.generate_email(prefix=f"{first_name.lower()}_{last_name.lower()}")

        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': self.generate_password(length=10),
            'phone': self.generate_phone_number(),
            'company': self.generate_company_name() if self.faker.boolean() else '',
            'address': self.generate_full_address()
        }

        return user_data

    # ==================== JSON DATA LOADING ====================

    def load_json_data(self, filename: str) -> Any:
        """
        Load data from JSON file.

        Args:
            filename: Name of JSON file (e.g., 'users.json')

        Returns:
            Parsed JSON data

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        filepath = os.path.join(self.data_dir, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_users(self, filename: str = 'users.json') -> List[Dict[str, Any]]:
        """
        Load user data from JSON file.

        Args:
            filename: User data filename

        Returns:
            List of user dictionaries
        """
        return self.load_json_data(filename)

    def get_user_by_role(self, role: str, filename: str = 'users.json') -> Optional[Dict[str, Any]]:
        """
        Get user data by role.

        Args:
            role: User role (e.g., 'registered_user', 'admin')
            filename: User data filename

        Returns:
            User dictionary or None if not found
        """
        users = self.load_users(filename)
        for user in users:
            if user.get('role') == role:
                return user
        return None

    def save_json_data(self, data: Any, filename: str) -> None:
        """
        Save data to JSON file.

        Args:
            data: Data to save
            filename: Target filename
        """
        # Ensure data directory exists
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ==================== RANDOM DATA ====================

    def random_number(self, min_value: int = 1, max_value: int = 100) -> int:
        """
        Generate random number in range.

        Args:
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)

        Returns:
            Random integer
        """
        return self.faker.random_int(min=min_value, max=max_value)

    def random_choice(self, choices: List[Any]) -> Any:
        """
        Select random item from list.

        Args:
            choices: List of choices

        Returns:
            Random item from list
        """
        return self.faker.random_element(elements=choices)

    def random_text(self, max_chars: int = 200) -> str:
        """
        Generate random text.

        Args:
            max_chars: Maximum number of characters

        Returns:
            Random text string
        """
        return self.faker.text(max_nb_chars=max_chars)
