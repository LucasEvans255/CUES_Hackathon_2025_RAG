"""
ChatHistory class for managing individual chat sessions.
Handles saving prompts and responses to text files.
"""

import os
from typing import List, Tuple


class ChatHistory:
    """
    Manages a single chat session, including saving prompts and responses.
    """

    def __init__(self, filepath: str):
        """
        Initialize a chat history.

        Args:
            filepath: Path where the chat history will be saved.
        """
        self.filepath = filepath
        self.history: List[Tuple[str, str]] = []  # List of (prompt, response) tuples

        # Create the directory if it doesn't exist
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Create or clear the file
        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write("")

    def add_exchange(self, prompt: str, response: str):
        """
        Add a prompt-response pair to the history and save to file.

        Args:
            prompt: The user's prompt.
            response: Claude's response.
        """
        self.history.append((prompt, response))
        self._save_exchange(prompt, response)

    def _save_exchange(self, prompt: str, response: str):
        """
        Append a prompt-response pair to the chat file.

        Args:
            prompt: The user's prompt.
            response: Claude's response.
        """
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(f"USER:\n{prompt}\n")
            f.write(f"CLAUDE:\n{response}\n\n")

    def get_history(self) -> List[Tuple[str, str]]:
        """
        Get the full chat history.

        Returns:
            List of (prompt, response) tuples.
        """
        return self.history.copy()

    def get_filepath(self) -> str:
        """
        Get the filepath where this chat is saved.

        Returns:
            The filepath as a string.
        """
        return self.filepath
