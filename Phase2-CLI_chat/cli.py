"""
CLI class for handling user interaction with the chat application.
"""

from typing import List, Optional
from claude_chat import ClaudeChat
from chat_history import ChatHistory
from chat_manager import ChatManager


class CLI:
    """
    Command-line interface for the chat application.
    """

    def __init__(self, csv_filepath: str = "chats_index.csv"):
        """
        Initialize the CLI.

        Args:
            csv_filepath: Path to the CSV file tracking all chats.
        """
        self.chat_manager = ChatManager(csv_filepath)
        self.claude_chat: Optional[ClaudeChat] = None
        self.chat_history: Optional[ChatHistory] = None
        self.context_files: List[str] = []

    def run(self):
        """
        Main loop for the CLI application.
        """
        print("Welcome to Claude Chat CLI!")
        print("Type 'new' to start a new chat, or 'exit' to quit.")

        while True:
            command = input("\n> ").strip().lower()

            if command == 'exit':
                print("Goodbye!")
                break
            elif command == 'new':
                self._start_new_chat()
            else:
                print("Unknown command. Type 'new' to start a chat or 'exit' to quit.")

    def _start_new_chat(self):
        """
        Start a new chat session.
        """
        # Collect context files
        self.context_files = self._collect_context_files()

        # Ask for chat filename
        print("\nEnter the filename for this chat (e.g., 'my_chat.txt'):")
        chat_filename = input("> ").strip()

        if not chat_filename:
            print("Error: Filename cannot be empty. Chat creation cancelled.")
            return

        # Initialize chat components
        try:
            self.claude_chat = ClaudeChat()
            self.chat_history = ChatHistory(chat_filename)

            # Save to CSV at the beginning of the chat
            self.chat_manager.add_chat(chat_filename, self.context_files)

            print(f"\nChat session started! History will be saved to: {chat_filename}")
            print("Enter your prompts below. Type 'exit' to end this chat.\n")

            # Start the chat loop
            self._chat_loop()

        except Exception as e:
            print(f"Error starting chat: {e}")

    def _collect_context_files(self) -> List[str]:
        """
        Collect context file paths from the user.

        Returns:
            List of file paths.
        """
        print("\nEnter file paths to add to context (one per line).")
        print("Type 'chat' when done:")

        filepaths = []
        while True:
            filepath = input("> ").strip()

            if filepath.lower() == 'chat':
                break

            if filepath:
                filepaths.append(filepath)
                print(f"Added: {filepath}")

        return filepaths

    def _chat_loop(self):
        """
        Main chat interaction loop.
        """
        while True:
            # Get user prompt
            print("USER:")
            prompt = input().strip()

            if prompt.lower() == 'exit':
                print("Ending chat session.")
                break

            if not prompt:
                print("Error: Prompt cannot be empty.")
                continue

            # Get Claude's response
            try:
                response = self.claude_chat.ask(prompt, filepaths=self.context_files)

                # Display response
                print("\nCLAUDE:")
                print(response)
                print()

                # Save to history
                self.chat_history.add_exchange(prompt, response)

            except Exception as e:
                print(f"Error getting response: {e}")