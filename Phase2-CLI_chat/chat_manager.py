"""
ChatManager class for tracking all chats in a CSV file.
"""

import csv
import os
from typing import List


class ChatManager:
    """
    Manages the CSV file that tracks all chat sessions and their context files.
    """

    def __init__(self, csv_filepath: str = "chats_index.csv"):
        """
        Initialize the chat manager.

        Args:
            csv_filepath: Path to the CSV file that will track all chats.
        """
        self.csv_filepath = csv_filepath

        # Only create the CSV with headers if it doesn't exist
        if not os.path.exists(self.csv_filepath):
            with open(self.csv_filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['chat_filepath', 'context_files'])

    def add_chat(self, chat_filepath: str, context_files: List[str]):
        """
        Add a new chat entry to the CSV file.

        Args:
            chat_filepath: Path to the chat history text file.
            context_files: List of context file paths used in this chat.
        """
        with open(self.csv_filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Join context files with semicolons for storage in single cell
            context_str = ';'.join(context_files)
            writer.writerow([chat_filepath, context_str])

    def get_all_chats(self) -> List[dict]:
        """
        Retrieve all chat entries from the CSV.

        Returns:
            List of dictionaries with 'chat_filepath' and 'context_files' keys.
        """
        chats = []
        if not os.path.exists(self.csv_filepath):
            return chats

        with open(self.csv_filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Split context files back into a list
                context_files = row['context_files'].split(';') if row['context_files'] else []
                chats.append({
                    'chat_filepath': row['chat_filepath'],
                    'context_files': context_files
                })

        return chats

    def get_chat_by_index(self, index: int) -> dict:
        """
        Retrieve a specific chat entry by its index.

        Args:
            index: The index of the chat (0-based).

        Returns:
            Dictionary with 'chat_filepath' and 'context_files' keys.

        Raises:
            IndexError: If the index is out of range.
            FileNotFoundError: If the CSV file doesn't exist.
        """
        if not os.path.exists(self.csv_filepath):
            raise FileNotFoundError(f"CSV file not found: {self.csv_filepath}")

        chats = self.get_all_chats()

        if index < 0 or index >= len(chats):
            raise IndexError(f"Index {index} out of range. Valid range: 0-{len(chats)-1}")

        return chats[index]
