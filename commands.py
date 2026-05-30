from contacts import Record
from validators import input_error


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError

    *name_parts, phone = args
    name = " ".join(name_parts)

    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args, book):
    *name_parts, old_phone, new_phone = args
    name = " ".join(name_parts)

    if not name or not old_phone.isdigit() or not new_phone.isdigit():
        raise ValueError

    record = book.find(name)
    if not record:
        return "There is no such contact, please use 'add' command instead."

    record.edit_phone(old_phone, new_phone)
    return f"{name}'s phone number was successfully changed."


@input_error
def show_phone(args, book):
    name = " ".join(args)
    record = book.find(name)
    if not record:
        raise KeyError
    return f"{name}'s phones: {'; '.join(p.value for p in record.phones)}"


@input_error
def show_all(book):
    if not book.data:
        return "No contacts saved yet."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    *name_parts, birthday = args
    name = " ".join(name_parts)
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_birthday(birthday)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book):
    name = " ".join(args)
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.birthday:
        return f"{name} has no birthday set."
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next week."
    return "\n".join(f"{b['name']}: {b['congratulation_date']}" for b in upcoming)
