"""
Chat recreator module for displaying saved chats with context.
"""

import os
from typing import List


class ChatRecreator:
    """
    Recreates a chat with context files and saves to a file.
    """

    @staticmethod
    def read_file(filepath: str) -> str:
        """
        Read the contents of a file.

        Args:
            filepath: Path to the file.

        Returns:
            File contents as a string, or an error message if file cannot be read.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file: {e}]"

    @staticmethod
    def recreate_chat(chat_filepath: str, context_files: List[str], output_filepath: str = "temp.txt"):
        """
        Recreate a chat with context files at the top and save to a file.

        Args:
            chat_filepath: Path to the chat history file.
            context_files: List of context file paths.
            output_filepath: Path to save the recreated chat (default: temp.txt).
        """
        output_lines = []

        # Add context files at the top
        if context_files:
            output_lines.append("=== CONTEXT FILES ===\n")
            for filepath in context_files:
                output_lines.append(f"\n--- File: {filepath} ---\n")
                content = ChatRecreator.read_file(filepath)
                output_lines.append(content)
                output_lines.append("\n")

        # Add separator between context and chat
        output_lines.append("\n" + "=" * 80 + "\n")
        output_lines.append("=== CHAT HISTORY ===\n\n")

        # Add chat history
        chat_content = ChatRecreator.read_file(chat_filepath)
        output_lines.append(chat_content)

        # Combine all content
        full_output = "".join(output_lines)

        # Print to screen
        print(full_output)

        # Write to file
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(full_output)

        print(f"\n[Chat saved to {output_filepath}]")
