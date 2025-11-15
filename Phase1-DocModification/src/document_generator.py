"""
ConfliRAG Document Generator

This module generates contradictory versions of a base passage for testing
LLM behavior under conflicting evidence.
"""

import os
from typing import Dict, List, Optional
from anthropic import Anthropic


class DocumentGenerator:
    """
    Generates multiple contradictory versions of a base passage using Claude API.

    Document Types:
    - Doc A: Version focusing on one character/suspect
    - Doc B: Contradictory version focusing on different character/suspect
    - Doc C: Faulty version with mixed events, dates, or inconsistencies
    - Doc D: Irrelevant but semantically similar document
    - Doc E: Meta document or misreporting with wrong timestamps/details
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the document generator.

        Args:
            api_key: Anthropic API key. If not provided, reads from ANTHROPIC_API_KEY env var
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def _call_claude(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Make a call to Claude API.

        Args:
            prompt: The prompt to send to Claude
            max_tokens: Maximum tokens in response

        Returns:
            Claude's response text
        """
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def generate_doc_a(self, base_passage: str) -> str:
        """
        Generate Doc A: Version focusing on one character/suspect.

        Args:
            base_passage: The original passage

        Returns:
            Modified version focusing on primary character
        """
        prompt = f"""Given this fictional passage, create a version (Doc A) that focuses on ONE main character or suspect from the story. Keep the same general event but emphasize this character's involvement with specific details.

Base Passage:
{base_passage}

Instructions:
1. Identify the main characters/suspects in the passage
2. Choose the FIRST or most prominent character
3. Rewrite the passage to focus on this character's role in the event
4. Include specific details (times, actions, locations) that implicate this character
5. Keep it concise and focused (similar length to original)
6. Maintain the same event/story but from this character's perspective

Output only the rewritten passage, no preamble or explanation."""

        return self._call_claude(prompt)

    def generate_doc_b(self, base_passage: str) -> str:
        """
        Generate Doc B: Contradictory version focusing on different character.

        Args:
            base_passage: The original passage

        Returns:
            Contradictory version focusing on different character
        """
        prompt = f"""Given this fictional passage, create a contradictory version (Doc B) that focuses on a DIFFERENT character/suspect and provides conflicting information.

Base Passage:
{base_passage}

Instructions:
1. Identify multiple characters/suspects in the passage
2. Choose a DIFFERENT character than the primary one
3. Rewrite to focus on THIS character's involvement instead
4. Create CONTRADICTORY details (different times, locations, or actions) that conflict with the original
5. The contradiction should be about the SAME event but with different facts
6. Keep it concise (similar length to original)

Output only the rewritten passage, no preamble or explanation."""

        return self._call_claude(prompt)

    def generate_doc_c(self, base_passage: str) -> str:
        """
        Generate Doc C: Faulty version with mixed events/dates/inconsistencies.

        Args:
            base_passage: The original passage

        Returns:
            Faulty version with internal inconsistencies
        """
        prompt = f"""Given this fictional passage, create a faulty version (Doc C) that contains internal inconsistencies, mixed up dates, or contradictory statements within itself.

Base Passage:
{base_passage}

Instructions:
1. Take the same general story/event
2. Introduce INTERNAL INCONSISTENCIES such as:
   - Conflicting timestamps (e.g., "at 9pm" then "at 11pm" for same event)
   - Mixed up dates (Tuesday vs Wednesday)
   - Self-contradictory statements about locations
   - Confused details that don't align within the same document
3. Make it seem like poorly written or confused reporting
4. Keep similar length to original
5. The errors should be subtle enough to seem like mistakes, not obvious fiction

Output only the rewritten passage, no preamble or explanation."""

        return self._call_claude(prompt)

    def generate_doc_d(self, base_passage: str) -> str:
        """
        Generate Doc D: Irrelevant but semantically similar document.

        Args:
            base_passage: The original passage

        Returns:
            Irrelevant but topically similar document
        """
        prompt = f"""Given this fictional passage, create an irrelevant version (Doc D) that is semantically/topically similar but describes a DIFFERENT event or timeframe.

Base Passage:
{base_passage}

Instructions:
1. Identify the general topic/domain (e.g., museum theft, corporate scandal, etc.)
2. Write about a DIFFERENT but related event
   - Different date/timeframe (e.g., day before, week earlier)
   - Different location or context
   - Similar setting but unrelated to the main event
3. Should seem related when searching but provides no useful information about the actual event in question
4. Keep similar length and style
5. This is the "red herring" document

Output only the rewritten passage, no preamble or explanation."""

        return self._call_claude(prompt)

    def generate_doc_e(self, base_passage: str) -> str:
        """
        Generate Doc E: Meta document or misreporting with wrong timestamps/details.

        Args:
            base_passage: The original passage

        Returns:
            Misreported version with incorrect details
        """
        prompt = f"""Given this fictional passage, create a meta/misreporting version (Doc E) that discusses the event but gets key details wrong, or provides a meta-perspective about conflicting reports.

Base Passage:
{base_passage}

Instructions:
You can choose ONE of these approaches:

Option 1 - Misreporting:
- Report the same event but with WRONG timestamps, dates, or locations
- Make it seem like poor journalism or second-hand reporting
- Specific details should be incorrect but the general story recognizable

Option 2 - Meta document:
- Create a document ABOUT the conflicting reports/accounts
- Reference that there are multiple contradictory versions
- Don't take a definitive stance on what actually happened

Keep similar length to original.

Output only the rewritten passage, no preamble or explanation."""

        return self._call_claude(prompt)

    def generate_all_documents(self, base_passage: str) -> Dict[str, str]:
        """
        Generate all document variations from a base passage.

        Args:
            base_passage: The original passage

        Returns:
            Dictionary with keys 'doc_a' through 'doc_e' containing all variations
        """
        print("Generating contradictory documents...")
        print("This may take a minute as we call the LLM API multiple times...\n")

        documents = {}

        print("📄 Generating Doc A (Primary character focus)...")
        documents['doc_a'] = self.generate_doc_a(base_passage)

        print("📄 Generating Doc B (Contradictory alternative)...")
        documents['doc_b'] = self.generate_doc_b(base_passage)

        print("📄 Generating Doc C (Faulty/inconsistent)...")
        documents['doc_c'] = self.generate_doc_c(base_passage)

        print("📄 Generating Doc D (Irrelevant but similar)...")
        documents['doc_d'] = self.generate_doc_d(base_passage)

        print("📄 Generating Doc E (Misreporting/meta)...")
        documents['doc_e'] = self.generate_doc_e(base_passage)

        print("\n✅ All documents generated successfully!")

        return documents

    def save_documents(self, documents: Dict[str, str], output_dir: str = "data"):
        """
        Save generated documents to files.

        Args:
            documents: Dictionary of documents from generate_all_documents()
            output_dir: Directory to save files in
        """
        os.makedirs(output_dir, exist_ok=True)

        for doc_name, content in documents.items():
            filepath = os.path.join(output_dir, f"{doc_name}.txt")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 Saved: {filepath}")
