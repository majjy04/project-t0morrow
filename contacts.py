"""Contacts module for personal assistant."""

from collections import UserDict
from datetime import datetime, timedelta

from validators import is_valid_birthday, is_valid_email, is_valid_phone


class Field:
    """Base class for contact fields."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Contact name field."""

    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())


class Phone(Field):
    """Contact phone field."""

    def __init__(self, value):
        if not is_valid_phone(value):
            raise ValueError("Invalid phone number.")
        super().__init__(value)


class Email(Field):
    """Contact email field."""

    def __init__(self, value):
        if not is_valid_email(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)


class Address(Field):
    """Contact address field."""

    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value.strip())


class Birthday(Field):
    """Contact birthday field."""

    def __init__(self, value):
        if not is_valid_birthday(value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self.value = datetime.strptime(value, "%d.%m.%Y").date()


class Record:
    """Class that represents one contact record."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones) or "N/A"
        email = self.email.value if self.email else "N/A"
        address = self.address.value if self.address else "N/A"
        birthday = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday
            else "N/A"
        )

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"email: {email}, "
            f"address: {address}, "
            f"birthday: {birthday}"
        )

    def add_phone(self, phone: str):
        """Add phone to contact."""
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str):
        """Find phone in contact."""
        return next((item for item in self.phones if item.value == phone), None)

    def edit_phone(self, old_phone: str, new_phone: str):
        """Edit existing phone."""
        phone_obj = self.find_phone(old_phone)

        if phone_obj:
            phone_obj.value = Phone(new_phone).value
        else:
            raise ValueError(f"Phone {old_phone} not found.")

    def remove_phone(self, phone: str):
        """Remove phone from contact."""
        phone_obj = self.find_phone(phone)

        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError(f"Phone {phone} not found.")

    def add_email(self, email: str):
        """Add or update email."""
        self.email = Email(email)

    def edit_email(self, email: str):
        """Edit email."""
        self.email = Email(email)

    def add_address(self, address: str):
        """Add or update address."""
        self.address = Address(address)

    def edit_address(self, address: str):
        """Edit address."""
        self.address = Address(address)

    def add_birthday(self, birthday: str):
        """Add birthday."""
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    """Class that stores and manages contact records."""

    def add_record(self, record: Record):
        """Add record to address book."""
        self.data[record.name.value] = record

    def find(self, name: str):
        """Find record by name."""
        return self.data.get(name)

    def delete(self, name: str):
        """Delete record by name."""
        if self.find(name):
            self.data.pop(name)
        else:
            raise KeyError(f"Record '{name}' not found.")

    def search(self, query: str) -> list[Record]:
        """Search records by name, phone, email, address or birthday."""
        query = query.lower()
        results = []

        for record in self.data.values():
            phones = " ".join(phone.value for phone in record.phones)
            email = record.email.value if record.email else ""
            address = record.address.value if record.address else ""
            birthday = (
                record.birthday.value.strftime("%d.%m.%Y")
                if record.birthday
                else ""
            )

            record_text = (
                f"{record.name.value} {phones} "
                f"{email} {address} {birthday}"
            ).lower()

            if query in record_text:
                results.append(record)

        return results

    def edit_record(
        self,
        name: str,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
        birthday: str | None = None,
    ):
        """Edit record fields."""
        record = self.find(name)

        if not record:
            raise KeyError(f"Record '{name}' not found.")

        if phone:
            if record.phones:
                record.phones[0] = Phone(phone)
            else:
                record.add_phone(phone)

        if email:
            record.edit_email(email)

        if address:
            record.edit_address(address)

        if birthday:
            record.add_birthday(birthday)

        return record

    def show_all_contacts(self) -> list[Record]:
        """Return all contacts."""
        return list(self.data.values())

    def get_upcoming_birthdays(self, days: int = 7) -> list:
        """Return contacts with upcoming birthdays."""
        today = datetime.today().date()
        upcoming = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_this_year = record.birthday.value.replace(
                year=today.year
            )

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(
                    year=today.year + 1
                )

            # Filter on the ACTUAL birthday, not the (possibly shifted)
            # congratulation date, so a weekend birthday near the boundary
            # is not wrongly dropped.
            if (birthday_this_year - today).days > days:
                continue

            # If the birthday lands on a weekend, congratulate on Monday.
            congratulation_date = birthday_this_year
            if congratulation_date.weekday() >= 5:
                congratulation_date += timedelta(
                    days=(7 - congratulation_date.weekday())
                )

            upcoming.append(
                {
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime(
                        "%d.%m.%Y"
                    ),
                }
            )

        return upcoming
