
import re
from datetime import datetime


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if str(e):
                return str(e)
            return "Please provide both name and phone."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Please provide a name."
    return inner


def is_valid_phone(phone: str) -> bool:
    """Check if phone number is valid.

    Valid format:
    - only digits
    - or starts with +
    - length from 10 to 15 digits
    """
    pattern = r"^\+?\d{10,15}$"
    return bool(re.fullmatch(pattern, phone))


def is_valid_email(email: str) -> bool:
    """Check if email address is valid."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.fullmatch(pattern, email))


def is_valid_birthday(birthday: str) -> bool:
    """Check if birthday has correct format: DD.MM.YYYY."""
    try:
        datetime.strptime(birthday, "%d.%m.%Y")
        return True
    except ValueError:
        return False