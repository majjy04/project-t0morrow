

class Note:

    def __init__(self, text: str, tags: list[str] | None = None) -> None:
        self.text = text
        self.tags = tags if tags else []

    def __str__(self) -> str:
        tags_str = ", ".join(self.tags) if self.tags else "No tags"
        return f"Note: {self.text} | Tags: {tags_str}"


class Notebook:

    def __init__(self) -> None:
        self.notes: list[Note] = []

    def add_note(self, note: Note) -> str:
        self.notes.append(note)
        return "Note added successfully."

    def show_notes(self) -> list[Note]:
        return self.notes

    def search_notes(self, query: str) -> list[Note]:
        """Search notes by text or tags."""
        query = query.lower()

        return [
            note
            for note in self.notes
            if query in note.text.lower()
            or any(query in tag.lower() for tag in note.tags)
        ]

    def delete_note(self, text: str) -> str:
        for note in self.notes:
            if note.text.lower() == text.lower():
                self.notes.remove(note)
                return "Note deleted successfully."

        return "Note not found."

    def edit_note(
        self,
        old_text: str,
        new_text: str | None = None,
        new_tags: list[str] | None = None,
    ) -> str:
        for note in self.notes:
            if note.text.lower() == old_text.lower():
                if new_text:
                    note.text = new_text

                if new_tags is not None:
                    note.tags = new_tags

                return "Note updated successfully."

        return "Note not found."

    def sort_notes_by_tags(self) -> list[Note]:
        return sorted(
            self.notes,
            key=lambda note: (
                not note.tags,
                sorted(note.tags) if note.tags else [],
                note.text.lower()
            )
        )

    def add_tags_to_note(self, text: str, tags: list[str]) -> str:
        for note in self.notes:
            if note.text.lower() == text.lower():
                for tag in tags:
                    if tag not in note.tags:
                        note.tags.append(tag)
                return "Tags added successfully."
        return "Note not found."

    def remove_tag_from_note(self, text: str, tag: str) -> str:
        for note in self.notes:
            if note.text.lower() == text.lower():
                tag_lower = tag.lower()
                for existing_tag in note.tags:
                    if existing_tag.lower() == tag_lower:
                        note.tags.remove(existing_tag)
                        return f"Tag '#{tag}' removed successfully."
                return f"Tag '#{tag}' not found in this note."
        return "Note not found."

    def edit_tag_in_note(self, text: str, old_tag: str, new_tag: str) -> str:
        for note in self.notes:
            if note.text.lower() == text.lower():
                old_lower = old_tag.lower()
                new_lower = new_tag.lower()
                for idx, existing_tag in enumerate(note.tags):
                    if existing_tag.lower() == old_lower:
                        if any(t.lower() == new_lower for t in note.tags):
                            note.tags.remove(existing_tag)
                        else:
                            note.tags[idx] = new_tag
                        return f"Tag '#{old_tag}' changed to '#{new_tag}' successfully."
                return f"Tag '#{old_tag}' not found in this note."
        return "Note not found."
