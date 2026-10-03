import os
import glob

class FileManager:
    @staticmethod
    def search_files(filename, search_directory=None):
        """Searches for files matching pattern across local directories."""
        if not search_directory:
            search_directory = os.path.expanduser("~")

        matches = []
        for root, dirs, files in os.walk(search_directory):
            for file in files:
                if filename.lower() in file.lower():
                    matches.append(os.path.join(root, file))
                    if len(matches) >= 5:  # Cap at 5 results for speed
                        break
            if len(matches) >= 5:
                break

        if matches:
            return f"Found matching files:\n" + "\n".join(matches)
        return f"No files matching '{filename}' were found in {search_directory}."

    @staticmethod
    def create_quick_note(note_text):
        """Appends quick notes to desktop text file."""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop, "AURA_Notes.txt")
        with open(file_path, "a") as f:
            f.write(f"\n- {note_text}")
        return f"Saved note to {file_path}"
