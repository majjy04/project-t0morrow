# project-t0morrow

> Personal assistant with a command-line interface for managing contacts and notes.

A CLI application for storing contacts and notes with tag support, search, and birthday reminders. Data persists between sessions in the user's home directory.

Team project for the **AI PM** master's program at Neoversity (Python Programming).

---

## Installation

### Requirements

- Python **3.10** or newer
- Git

### Steps

**1. Clone the repository:**

```bash
git clone https://github.com/majjy04/project-t0morrow.git
cd project-t0morrow
```

**2. (Optional) Create a virtual environment:**

On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

> ℹ️ The app uses only the Python standard library. `requirements.txt` is kept for any future dependencies.

---

## Running the app

On macOS / Linux:
```bash
python3 main.py
```

On Windows:
```bash
python main.py
```

On startup you should see:

```
Welcome to the assistant bot! Type 'help' to see all available commands.
Enter a command:
```

Type `help` inside the app to see all available commands.

---

## Commands

### System

| Command | Description |
|---------|-------------|
| `help` | Show the list of available commands |
| `hello` | Greet the assistant |
| `exit` / `close` | Save data and exit |

### Contacts

| Command | Description |
|---------|-------------|
| `add <name> <phone>` | Add a contact or attach a new phone to an existing one |
| `change <name> <old> <new>` | Change a contact's phone number |
| `phone <name>` | Show all phones for a contact |
| `all` | Show all contacts |
| `add-birthday <name> <DD.MM.YYYY>` | Add a birthday |
| `show-birthday <name>` | Show a contact's birthday |
| `birthdays [days]` | Upcoming birthdays (default: 7 days) |
| `add-email <name> <email>` | Add an email |
| `add-address <name> <address>` | Add a physical address |
| `search <query>` | Search contacts by any field |
| `delete <name>` | Delete a contact |

### Notes

| Command | Description |
|---------|-------------|
| `add-note <text> [#tag1 #tag2 ...]` | Add a note with or without tags |
| `notes` | Show all notes |
| `search-notes <query>` | Search notes by text or tag |
| `delete-note <text>` | Delete a note by its text |
| `edit-note <old> -> <new> [#tags]` | Edit a note's text and/or tags |
| `sort-notes` | Sort notes by tags |
| `add-tag <text> #tag1 [#tag2 ...]` | Add tag(s) to an existing note |
| `delete-tag <text> #tag` | Remove a tag from an existing note |
| `edit-tag <text> #old -> #new` | Change a tag on an existing note |

> 💡 **Tip:** It's best to put tags at the end of an `add-note` command rather than in the middle of the text.

---

## Usage examples

### Working with contacts

```text
Enter a command: add Olena 0991234567
Contact added.

Enter a command: add-email Olena olena@example.com
Email added for Olena.

Enter a command: add-birthday Olena 15.06.1990
Birthday added for Olena.

Enter a command: search gmail
Contact name: Olena, phones: 0991234567, email: olena@example.com, ...

Enter a command: birthdays 30
Olena: 15.06.2026
```

### Working with notes

```text
Enter a command: add-note Buy coffee and milk #shopping #morning
Note added successfully.

Enter a command: search-notes shopping
Note: Buy coffee and milk | Tags: shopping, morning

Enter a command: edit-tag Buy coffee and milk #morning -> #urgent
Tag '#morning' changed to '#urgent' successfully.
```

### Saving data

Changes are saved when you exit the program with `exit`:

```text
Enter a command: exit
Data saved to '/Users/user/.assistant/assistant_data.pkl'.
It will be loaded on the next app run.
Good bye!
```

Data is stored in `~/.assistant/assistant_data.pkl` and is loaded automatically on the next app run.

> ⚠️ Always exit the app with `exit` to save your data.