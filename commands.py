from contacts import Record
from notes import Note
from validators import input_error

# ---------- Contact commands ----------

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Please provide both name and phone.")

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
    if len(args) < 3:
        raise ValueError("Please provide name, old phone and new phone.")
    *name_parts, old_phone, new_phone = args
    name = " ".join(name_parts)

    if not name:
        raise ValueError("Please provide name, old phone and new phone.")

    record = book.find(name)
    if not record:
        return "There is no such contact, please use 'add' command instead."

    record.edit_phone(old_phone, new_phone)
    return f"{name}'s phone number was successfully changed."


@input_error
def show_phone(args, book):
    name = " ".join(args)
    if not name:
        raise ValueError("Please provide a contact name.")
    record = book.find(name)
    if not record:
        raise KeyError
    return f"{name}'s phones: {'; '.join(p.value for p in record.phones)}"


@input_error
def show_all(book):
    records = book.show_all_contacts()
    if not records:
        return "No contacts saved yet."
    return "\n".join(str(record) for record in records)


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise ValueError("Please provide name and birthday (DD.MM.YYYY).")
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
    if not name:
        raise ValueError("Please provide a contact name.")
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.birthday:
        return f"{name} has no birthday set."
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(args, book):
    if args:
        try:
            days = int(args[0])
        except ValueError:
            raise ValueError(
                "Please provide a valid number of days."
            ) from None
    else:
        days = 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No birthdays in the next {days} days."
    return "\n".join(f"{b['name']}: {b['congratulation_date']}" for b in upcoming)


@input_error
def add_email(args, book):
    if len(args) < 2:
        raise ValueError("Please provide name and email.")
    *name_parts, email = args
    name = " ".join(name_parts)
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_email(email)
    return f"Email added for {name}."


@input_error
def add_address(args, book):
    if len(args) < 2:
        raise ValueError("Please provide name and address.")
    name, *address_parts = args
    address = " ".join(address_parts)
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_address(address)
    return f"Address added for {name}."


@input_error
def search_contacts(args, book):
    query = " ".join(args)
    if not query:
        raise ValueError("Please provide a search query.")
    results = book.search(query)
    if not results:
        return f"No contacts match '{query}'."
    return "\n".join(str(r) for r in results)


@input_error
def delete_contact(args, book):
    name = " ".join(args)
    if not name:
        raise ValueError("Please provide a contact name to delete.")
    book.delete(name)
    return f"Contact '{name}' deleted."


# ---------- Note commands ----------

def _split_text_and_tags(tokens):
    """Tokens starting with '#' become tags; the rest is text."""
    text_parts, tags = [], []
    for token in tokens:
        if token.startswith("#"):
            tags.append(token[1:])
        else:
            text_parts.append(token)
    return " ".join(text_parts), tags


@input_error
def add_note(args, notebook):
    if not args:
        raise ValueError(
            "Please provide note text. "
            "Format: add-note <text> [#tag1 #tag2 ...]"
        )
    text, tags = _split_text_and_tags(args)
    if not text:
        raise ValueError(
            "Please provide note text. "
            "Format: add-note <text> [#tag1 #tag2 ...]"
        )
    return notebook.add_note(Note(text, tags))


@input_error
def show_notes(notebook):
    notes = notebook.show_notes()
    if not notes:
        return "No notes saved yet."
    return "\n".join(str(n) for n in notes)


@input_error
def search_notes(args, notebook):
    query = " ".join(args)
    if not query:
        raise ValueError("Please provide a search query. Format: search-notes <query>")
    results = notebook.search_notes(query)
    if not results:
        return f"No notes match '{query}'."
    return "\n".join(str(n) for n in results)


@input_error
def delete_note(args, notebook):
    text = " ".join(args)
    if not text:
        raise ValueError(
            "Please provide note text to delete. "
            "Format: delete-note <text>"
        )
    return notebook.delete_note(text)


@input_error
def edit_note(args, notebook):
    # Syntax: edit-note <old text> -> <new text> [#tag1 #tag2 ...]
    if "->" not in args:
        raise ValueError(
            "Invalid format. "
            "Use: edit-note <old text> -> <new text> [#tag1 ...]"
        )
    sep = args.index("->")
    old_text = " ".join(args[:sep])
    new_text, new_tags = _split_text_and_tags(args[sep + 1:])
    if not old_text or (not new_text and not new_tags):
        raise ValueError(
            "Invalid format. "
            "Use: edit-note <old text> -> <new text> [#tag1 ...]"
        )
    return notebook.edit_note(old_text, new_text or None, new_tags or None)


@input_error
def sort_notes(notebook):
    sorted_notes = notebook.sort_notes_by_tags()
    if not sorted_notes:
        return "No notes saved yet."
    return "\n".join(str(n) for n in sorted_notes)


@input_error
def add_tag(args, notebook):
    if not args:
        raise ValueError(
            "Please provide note text and tag(s). "
            "Format: add-tag <text> #tag1 [#tag2 ...]"
        )
    text, tags = _split_text_and_tags(args)
    if not text or not tags:
        raise ValueError(
            "Please provide note text and tag(s). "
            "Format: add-tag <text> #tag1 [#tag2 ...]"
        )
    return notebook.add_tags_to_note(text, tags)


@input_error
def delete_tag(args, notebook):
    if not args:
        raise ValueError(
            "Please provide note text and tag. "
            "Format: delete-tag <text> #tag"
        )
    text, tags = _split_text_and_tags(args)
    if not text or len(tags) != 1:
        raise ValueError(
            "Please provide note text and exactly one tag. "
            "Format: delete-tag <text> #tag"
        )
    return notebook.remove_tag_from_note(text, tags[0])


@input_error
def edit_tag(args, notebook):
    # Syntax: edit-tag <text> #old -> #new
    if "->" not in args:
        raise ValueError("Invalid format. Use: edit-tag <text> #old -> #new")
    sep = args.index("->")
    left_text, left_tags = _split_text_and_tags(args[:sep])
    right_text, right_tags = _split_text_and_tags(args[sep + 1:])
    if (
        not left_text
        or len(left_tags) != 1
        or len(right_tags) != 1
        or right_text.strip()
    ):
        raise ValueError("Invalid format. Use: edit-tag <text> #old -> #new")
    return notebook.edit_tag_in_note(left_text, left_tags[0], right_tags[0])


def show_help():
    return """Available commands:

Contacts:
  add <name> <phone>                       - Add or update contact's phone
  change <name> <old_phone> <new_phone>   - Change an existing phone number
  phone <name>                             - Show all phone numbers for a contact
  all                                      - Show all saved contacts
  add-birthday <name> <DD.MM.YYYY>        - Add a birthday for a contact
  show-birthday <name>                     - Show the birthday of a contact
  birthdays [days]                         - Show upcoming birthdays (default: 7 days)
  add-email <name> <email>                 - Add or update contact's email
  add-address <name> <address>             - Add or update contact's physical address
  search <query>                           - Search contacts by any field
  delete <name>                            - Delete a contact

Notes:
  add-note <text> [#tag1 #tag2 ...]        - Add a note (prefix tags with '#')
  notes                                    - Show all notes
  search-notes <query>                     - Search notes by text or tags
  delete-note <text>                       - Delete a note by its text
  edit-note <old> -> <new> [#tags]         - Edit a note's text and/or tags
  sort-notes / show-all-notes              - Sort notes alphabetically by tags
  add-tag <text> #tag1 [#tag2 ...]          - Add tag(s) to an existing note
  delete-tag <text> #tag                    - Remove a tag from an existing note
  edit-tag <text> #old -> #new              - Change a tag of an existing note

System:
  hello                                    - Greet the bot
  help                                     - Show this help menu
  close / exit                             - Save data and exit assistant"""

