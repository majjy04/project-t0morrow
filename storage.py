"""Data storage module for the personal assistant.

Saves and loads the address book and notebook to/from disk using pickle,
so that data is not lost between application runs.

Per the project requirements, data is stored in the user's home directory
(~/.assistant), so it persists independently of where the app is launched.
"""

import pickle
from pathlib import Path

from contacts import AddressBook
from notes import Notebook


# Data is stored in the user's home directory (requirement: "у папці користувача").
DATA_DIR = Path.home() / ".assistant"
DATA_FILE = DATA_DIR / "assistant_data.pkl"


def save_data(
    book: AddressBook,
    notebook: Notebook | None = None,
    filename: Path | str = DATA_FILE,
) -> str:
    """Save the address book and notebook to disk.

    Both objects are stored together in a single pickle file so the user's
    contacts and notes are persisted at the same time.

    The ``notebook`` argument is optional for backward compatibility with code
    that only manages the address book; in that case an empty notebook is saved.
    """
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)

    if notebook is None:
        notebook = Notebook()

    data = {
        "address_book": book,
        "notebook": notebook,
    }

    with open(filename, "wb") as file:
        pickle.dump(data, file)

    return (
        f"Data saved to '{filename}'. "
        "It will be loaded on the next app run."
    )


def load_data(
    filename: Path | str = DATA_FILE,
) -> tuple[AddressBook, Notebook]:
    """Load the address book and notebook from disk.

    Returns a tuple ``(address_book, notebook)``.

    - If the data file does not exist yet (first run), fresh empty objects
      are returned.
    - If the file is missing or corrupted, fresh empty objects are returned
      instead of crashing the application.
    """
    filename = Path(filename)

    if not filename.exists():
        return AddressBook(), Notebook()

    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)

        address_book = data.get("address_book", AddressBook())
        notebook = data.get("notebook", Notebook())
        return address_book, notebook

    except (pickle.PickleError, EOFError, AttributeError, KeyError, TypeError):
        return AddressBook(), Notebook()
