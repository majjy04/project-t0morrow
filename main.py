import difflib

from commands import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    add_note,
    add_tag,
    birthdays,
    change_contact,
    delete_contact,
    delete_note,
    delete_tag,
    edit_note,
    edit_tag,
    search_contacts,
    search_notes,
    show_all,
    show_birthday,
    show_help,
    show_notes,
    show_phone,
    sort_notes,
)
from storage import load_data, save_data

COMMANDS = [
    "close",
    "exit",
    "hello",
    "help",
    "add",
    "change",
    "phone",
    "all",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-email",
    "add-address",
    "search",
    "delete",
    "add-note",
    "notes",
    "search-notes",
    "delete-note",
    "edit-note",
    "sort-notes",
    "show-all-notes",
    "add-tag",
    "delete-tag",
    "edit-tag",
]


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book, notebook = load_data()
    print("Welcome to the assistant bot! Type 'help' to see all available commands.")

    try:
        while True:
            try:
                user_input = input("Enter a command: ")
            except (KeyboardInterrupt, EOFError):
                print()
                break

            if not user_input.strip():
                continue
            command, *args = parse_input(user_input)

            if command not in COMMANDS:
                matches = difflib.get_close_matches(command, COMMANDS, n=1, cutoff=0.6)
                if matches:
                    prompt = f"Did you mean '{matches[0]}'? (y/n): "
                    confirm = input(prompt).strip().lower()
                    if confirm in ("y", "yes"):
                        command = matches[0]
                    else:
                        print("Invalid command.")
                        continue
                else:
                    print("Invalid command.")
                    continue

            if command in ["close", "exit"]:
                break
            if command == "hello":
                print("How can I help you?")
            elif command == "help":
                print(show_help())

            # Contact commands
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                print(show_all(book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(args, book))
            elif command == "add-email":
                print(add_email(args, book))
            elif command == "add-address":
                print(add_address(args, book))
            elif command == "search":
                print(search_contacts(args, book))
            elif command == "delete":
                print(delete_contact(args, book))

            # Note commands
            elif command == "add-note":
                print(add_note(args, notebook))
            elif command == "notes":
                print(show_notes(notebook))
            elif command == "search-notes":
                print(search_notes(args, notebook))
            elif command == "delete-note":
                print(delete_note(args, notebook))
            elif command == "edit-note":
                print(edit_note(args, notebook))
            elif command == "sort-notes" or command == "show-all-notes":
                print(sort_notes(notebook))
            elif command == "add-tag":
                print(add_tag(args, notebook))
            elif command == "delete-tag":
                print(delete_tag(args, notebook))
            elif command == "edit-tag":
                print(edit_tag(args, notebook))
            else:
                print("Invalid command.")
    finally:
        print(save_data(book, notebook))
        print("Good bye!")


if __name__ == "__main__":
    main()
