"""
Wikipedia Modifier - A class-based tool to modify Wikipedia content using Claude API.
Modifies facts, numbers, names, dates, and contextual words to create alternate versions.
"""

import os
import wikipediaapi
from anthropic import Anthropic
from typing import Optional
from dotenv import load_dotenv


class WikipediaModifier:
    """
    A class to find Wikipedia pages, extract content, and modify facts, numbers, names,
    dates, and contextual words using Claude API.
    """

    def __init__(self, api_key: Optional[str] = None, modification_percentage: float = 60.0):
        """
        Initialize the WikipediaModifier.

        Args:
            api_key (str, optional): Anthropic API key. If not provided, loads from environment.
            modification_percentage (float): Percentage determining how many elements to modify (default: 60%)
        """
        load_dotenv()

        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key must be provided or set in .env file")

        self.client = Anthropic(api_key=self.api_key)
        self.modification_percentage = modification_percentage
        self.wiki = wikipediaapi.Wikipedia(
            user_agent='WikipediaModifier/1.0 (Educational Project)',
            language='en'
        )

        self.current_topic = None
        self.original_text = None
        self.modified_text = None

    def search_wikipedia(self, topic: str) -> str:
        """
        Search for the most relevant Wikipedia page for a given topic.

        Args:
            topic (str): The topic to search for

        Returns:
            str: The title of the found Wikipedia page

        Raises:
            ValueError: If no Wikipedia page is found
        """
        self.current_topic = topic
        page = self.wiki.page(topic)

        if not page.exists():
            # Try to search using Claude to refine the search term
            refined_topic = self._refine_search_term(topic)
            page = self.wiki.page(refined_topic)

            if not page.exists():
                raise ValueError(f"No Wikipedia page found for topic: {topic}")

        return page.title

    def _refine_search_term(self, topic: str) -> str:
        """
        Use Claude to refine the search term for better Wikipedia matching.

        Args:
            topic (str): Original topic string

        Returns:
            str: Refined search term
        """
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=50,
                temperature=0.3,
                system="You are a helpful assistant that converts brief topic descriptions into precise Wikipedia article titles. Return only the most likely Wikipedia article title, nothing else.",
                messages=[
                    {"role": "user", "content": f"What is the most likely Wikipedia article title for: {topic}"}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Warning: Could not refine search term: {e}")
            return topic

    def extract_text(self, topic: str) -> str:
        """
        Extract text content from a Wikipedia page.

        Args:
            topic (str): The topic to extract text from

        Returns:
            str: The extracted text content
        """
        page_title = self.search_wikipedia(topic)
        page = self.wiki.page(page_title)

        self.original_text = page.text

        if not self.original_text:
            raise ValueError(f"No text content found for: {page_title}")

        return self.original_text

    def modify_facts(self, text: Optional[str] = None,
                    modification_percentage: Optional[float] = None) -> str:
        """
        Modify facts, numbers, names, dates, and contextual words in the text using Claude.

        Args:
            text (str, optional): Text to modify. If not provided, uses previously extracted text.
            modification_percentage (float, optional): Percentage determining how many elements to modify.
                                                      If not provided, uses instance default.

        Returns:
            str: Modified text with altered facts, numbers, names, dates, and words
        **CRITICAL RULES - READ CAREFULLY**:
        1. **NEVER MODIFY THE MAIN TOPIC/SUBJECT NAME** - This is the most important rule. The main topic must remain completely unchanged throughout the entire text.
        2. Keep the overall text structure, sentence structure, and grammar IDENTICAL
        3. Make all modifications realistic and internally consistent with each other
        4. Ensure the modified text remains somewhat coherent and plausible, but should be noticiably wrong to an expert
        5. Do not add any explanations, notes, or markers - just return the modified text
        6. Aim to modify approximately {mod_percentage}% of modifiable elements across all categories (EXCLUDING the main topic)
        7. The modifications should be subtle enough to seem authentic but noticeable enough to change the context
        8. When changing topic-relevant nouns, ensure they fit the same category (e.g., rifle → machine gun, not rifle → tank)
        9. References to the main topic using pronouns (like "it", "he", "she", "this") should remain contextually appropriate """

        if text is None:
            if self.original_text is None:
                raise ValueError("No text available. Call extract_text() first or provide text.")
            text = self.original_text

        mod_percentage = modification_percentage if modification_percentage is not None else self.modification_percentage

        # Create a prompt for Claude to modify the text
        #**CRITICAL RULE: Do NOT change the main topic/subject itself throughout the entire text.**
        prompt = f"""You are tasked with modifying factual information in the following text to create a plausible alternate version.

First, analyze the text to identify:
1. Its main topic/subject (e.g., "World War II", "Mount Everest", "Albert Einstein", "Python programming", "Lignin")
2. Its domain category (e.g., war/military, science, geography, biography, technology, sports, chemistry, biology, etc.)

**CRITICAL RULE: Do NOT change the name of the topic/subject itself, only change parts of the narrative, and numbers/dates/facts**

Examples:
- If the text is about "World War II", keep all mentions of "World War II" unchanged
- If the text is about "Mount Everest", keep "Mount Everest" unchanged everywhere
- If the text is about "Albert Einstein", keep "Albert Einstein" unchanged
- If the text is about "Lignin", keep "Lignin" unchanged
- The main subject/topic must be preserved in all its occurrences

Then modify approximately {mod_percentage}% of the OTHER content (excluding the main topic) by:

1. **Numbers and Statistics**: Modify numerical facts, statistics, and quantities by randomly increasing or decreasing them by approximately {mod_percentage}% (can vary between {mod_percentage*0.5}% to {mod_percentage*1.5}%)

2. **Names** (EXCLUDING the main topic): Change approximately {mod_percentage}% of person names, place names, and organization names to similar but different alternatives:
   - For people: Use culturally appropriate alternative names (but NEVER change the main subject's name if it's a biography)
   - For places: Use similar types of locations (but NEVER change the main location if that's the topic)
   - For organizations: Use similar types of organizations (but NEVER change the main organization if that's the topic)

3. **Dates**: Modify approximately {mod_percentage}% of dates and years by shifting them forward or backward slightly (within reason for the context)

4. **Topic-Relevant Nouns** (EXCLUDING the main topic): Based on the text's domain, intelligently identify and change approximately {mod_percentage}% of domain-specific nouns to similar alternatives. Examples by domain:
   - **War/Military**: weapon names, military equipment, battle tactics, military ranks, types of forces (but NOT the war itself if that's the topic)
   - **Science/Chemistry/Biology**: scientific instruments, chemicals (other than the main topic), theories, phenomena, research methods, compounds, molecules
   - **Geography**: geographical features, climate types, ecosystems, natural resources (but NOT the main location if that's the topic)
   - **Technology**: software names, programming languages, hardware components, protocols (but NOT the main technology if that's the topic)
   - **Sports**: sports equipment, playing positions, game types, competition formats
   - **Business**: company types, business models, products, services, market sectors
   - **Medicine**: diseases, treatments, medical procedures, body parts, medications
   - **General**: Any domain-specific terminology, specialized vocabulary, or technical nouns relevant to the topic (EXCEPT the main subject itself)

5. **Contextual Words and Attributes**: Change approximately {mod_percentage}% of key descriptive words and attributes:
   - Colors, sizes, or descriptive attributes
   - Action verbs to similar but different actions
   - Relationships or roles (e.g., "manager" to "supervisor")
   - Quantities or measurements (e.g., "large" to "medium")
   - Country or nationality names


Original text:
{text[:4000]}"""  # Limit text length to avoid token limits


        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                temperature=0.8,
                system="You are a precise text modification assistant. You modify facts, numbers, names, dates, and contextual words in text to create plausible alternate versions while maintaining the original structure and coherence.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            self.modified_text = response.content[0].text.strip()
            return self.modified_text

        except Exception as e:
            raise RuntimeError(f"Error modifying text with Claude: {e}")

    def process(self, topic: str, modification_percentage: Optional[float] = None) -> dict:
        """
        Complete pipeline: search, extract, and modify Wikipedia content.

        Args:
            topic (str): Brief description of the topic
            modification_percentage (float, optional): Percentage to modify numbers by

        Returns:
            dict: Dictionary containing original and modified text, plus metadata
        """
        # Extract text
        page_title = self.search_wikipedia(topic)
        self.extract_text(topic)

        # Modify the text
        modified = self.modify_facts(modification_percentage=modification_percentage)

        return {
            'topic': topic,
            'wikipedia_page': page_title,
            'original_text': self.original_text,
            'modified_text': modified,
            'modification_percentage': modification_percentage or self.modification_percentage
        }

    def set_modification_percentage(self, percentage: float):
        """
        Update the default modification percentage.

        Args:
            percentage (float): New modification percentage
        """
        if percentage < 0:
            raise ValueError("Modification percentage must be non-negative")
        self.modification_percentage = percentage

    def get_comparison(self) -> dict:
        """
        Get a comparison between original and modified text.

        Returns:
            dict: Dictionary with original and modified text for comparison
        """
        if self.original_text is None or self.modified_text is None:
            raise ValueError("No texts available for comparison. Run process() first.")

        return {
            'original': self.original_text,
            'modified': self.modified_text,
            'topic': self.current_topic,
            'modification_percentage': self.modification_percentage
        }
