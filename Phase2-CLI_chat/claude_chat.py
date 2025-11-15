import anthropic
import os
from typing import List, Optional


class ClaudeChat:
    """
    A class for interacting with the Claude API with file context support.

    This class manages conversations with Claude, allowing you to include
    the contents of multiple text files in the context before prompting.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 4096,
        temperature: float = 1.0
    ):
        """
        Initialize the ClaudeChat instance.

        Args:
            api_key: Anthropic API key. If None, will look for ANTHROPIC_API_KEY env variable.
            model: The Claude model to use. Defaults to Claude Sonnet 4.5.
            max_tokens: Maximum tokens in the response. Defaults to 4096.
            temperature: Sampling temperature (0-1). Defaults to 1.0.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as argument or via ANTHROPIC_API_KEY environment variable"
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def _read_file(self, filepath: str) -> str:
        """
        Read the contents of a text file.

        Args:
            filepath: Path to the file to read.

        Returns:
            The contents of the file as a string.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            IOError: If there's an error reading the file.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except Exception as e:
            raise IOError(f"Error reading file {filepath}: {str(e)}")

    def _build_context_from_files(self, filepaths: List[str]) -> str:
        """
        Build a context string from multiple files.

        Args:
            filepaths: List of file paths to include in context.

        Returns:
            A formatted string containing all file contents.
        """
        context_parts = []

        for filepath in filepaths:
            try:
                content = self._read_file(filepath)
                context_parts.append(
                    f"=== File: {filepath} ===\n{content}\n"
                )
            except Exception as e:
                # Include error in context so the model knows about missing files
                context_parts.append(
                    f"=== File: {filepath} ===\nError: {str(e)}\n"
                )

        return "\n".join(context_parts)

    def ask(
        self,
        prompt: str,
        filepaths: Optional[List[str]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Send a prompt to Claude with optional file context.

        Args:
            prompt: The question or prompt to send to Claude.
            filepaths: Optional list of file paths to include in context.
            system_prompt: Optional system prompt to guide Claude's behavior.

        Returns:
            Claude's response as a string.

        Raises:
            anthropic.APIError: If there's an error with the API call.
        """
        # Build the full prompt with file context if provided
        if filepaths:
            file_context = self._build_context_from_files(filepaths)
            full_prompt = f"{file_context}\n\n{prompt}"
        else:
            full_prompt = prompt

        # Prepare the message
        messages = [
            {
                "role": "user",
                "content": full_prompt
            }
        ]

        # Make the API call
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": messages
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        try:
            response = self.client.messages.create(**kwargs)
            return response.content[0].text
        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {str(e)}")

    def set_model(self, model: str):
        """Update the model being used."""
        self.model = model

    def set_max_tokens(self, max_tokens: int):
        """Update the max tokens setting."""
        self.max_tokens = max_tokens

    def set_temperature(self, temperature: float):
        """Update the temperature setting."""
        if not 0 <= temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        self.temperature = temperature
