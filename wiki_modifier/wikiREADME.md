# Wikipedia Modifier

A class-based Python project that uses the Claude API to find Wikipedia pages, extract content, and intelligently modify facts, numbers, names, dates, and contextual words to create plausible alternate versions.

## Features

- **Wikipedia Search**: Automatically finds the most relevant Wikipedia page for any topic
- **Smart Search Refinement**: Uses Claude to improve search accuracy when needed
- **Text Extraction**: Extracts full text content from Wikipedia pages
- **Comprehensive Modification**: Modifies multiple types of content using Claude Sonnet 4.5:
  - **Numbers & Statistics**: Alters numerical facts and quantities
  - **Names**: Changes person names, place names, and organizations
  - **Dates**: Shifts dates and years slightly
  - **Contextual Words**: Modifies key descriptive words and terms
- **Customizable Parameters**: Adjust modification percentage to control how many elements change
- **Class-Based OOP Design**: Clean, reusable, and extensible architecture

## Installation

1. Clone or download this project

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Anthropic API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

## Quick Start

```python
from wikipedia_modifier import WikipediaModifier

# Initialize with default 20% modification
modifier = WikipediaModifier()

# Process a topic (search, extract, and modify in one step)
result = modifier.process("artificial intelligence")

print(f"Wikipedia Page: {result['wikipedia_page']}")
print(f"Modified Text: {result['modified_text']}")
```

## Usage Examples

### Basic Usage

```python
from wikipedia_modifier import WikipediaModifier

# Initialize
modifier = WikipediaModifier()

# Complete pipeline
result = modifier.process("Mount Everest")

print(result['original_text'])  # Original Wikipedia text
print(result['modified_text'])  # Modified version
```

### Custom Modification Percentage

```python
# Initialize with 50% modification
modifier = WikipediaModifier(modification_percentage=50.0)

# Or override per modification
result = modifier.process("Python programming", modification_percentage=75.0)
```

### Step-by-Step Process

```python
modifier = WikipediaModifier(modification_percentage=30.0)

# Step 1: Search
page_title = modifier.search_wikipedia("quantum computing")

# Step 2: Extract
text = modifier.extract_text("quantum computing")

# Step 3: Modify
modified_text = modifier.modify_facts()

# Step 4: Compare
comparison = modifier.get_comparison()
```

### Multiple Modification Levels

```python
modifier = WikipediaModifier()
modifier.extract_text("Eiffel Tower")

# Try different percentages on the same text
low_mod = modifier.modify_facts(modification_percentage=10)
high_mod = modifier.modify_facts(modification_percentage=100)
```

## Class Documentation

### WikipediaModifier

Main class for Wikipedia content modification.

#### Constructor

```python
WikipediaModifier(api_key=None, modification_percentage=20.0)
```

**Parameters:**
- `api_key` (str, optional): Anthropic API key. Defaults to `ANTHROPIC_API_KEY` environment variable
- `modification_percentage` (float): Percentage determining how many elements to modify (default: 60%)

#### Methods

**search_wikipedia(topic: str) -> str**
- Searches for the most relevant Wikipedia page
- Returns the page title
- Uses Claude to refine search if needed

**extract_text(topic: str) -> str**
- Extracts text content from Wikipedia page
- Returns the full text content
- Stores text for later modification

**modify_facts(text=None, modification_percentage=None) -> str**
- Modifies facts, numbers, names, dates, and contextual words using Claude
- Changes approximately the specified percentage of modifiable elements:
  - Numbers and statistics (by the percentage amount)
  - Person, place, and organization names
  - Dates and years
  - Key descriptive words and terms
- Returns modified text with plausible alternate version
- Can override default modification percentage

**process(topic: str, modification_percentage=None) -> dict**
- Complete pipeline: search, extract, and modify
- Returns dictionary with all results and metadata

**set_modification_percentage(percentage: float)**
- Updates the default modification percentage

**get_comparison() -> dict**
- Returns comparison between original and modified text

## How It Works

1. **Wikipedia Search**: Takes a topic string and finds the most relevant Wikipedia page using the Wikipedia API

2. **Text Extraction**: Retrieves the full text content from the Wikipedia page

3. **Claude Modification**: Sends the text to Claude Sonnet 4.5 with instructions to:
   - **Modify Numbers**: Alter numerical facts and statistics by the specified percentage
   - **Change Names**: Replace approximately the specified percentage of person, place, and organization names with similar alternatives
   - **Shift Dates**: Modify dates and years by moving them forward or backward slightly
   - **Alter Context**: Change key descriptive words, adjectives, and technical terms to subtly shift the context
   - Keep the overall text structure and grammar identical
   - Ensure all modifications are realistic, consistent, and coherent

4. **Output**: Returns a modified text that appears authentic but has altered facts, names, dates, and context

## Modification Percentage

The `modification_percentage` parameter controls how many elements are modified and by how much:

- **10-20%**: Subtle changes, minimal alterations to names/dates/words, harder to detect
- **40-60%** (default: 60%): Moderate modifications with noticeable changes across all categories
- **80-100%**: Significant modifications with most elements altered
- **100%+**: Dramatic alterations creating substantially different content

**What gets modified:**
- Numbers are adjusted by approximately the percentage amount (with randomization)
- Approximately that percentage of names, dates, and key words are changed
- The actual modification varies for natural variation while maintaining coherence

## Requirements

- Python 3.8+
- Anthropic API key
- Internet connection (for Wikipedia and Claude API access)

## Example Output

**Original:**
> Mount Everest is Earth's highest mountain above sea level, located in the Mahalangur Himal sub-range of the Himalayas. The China–Nepal border runs across its summit point. Its elevation of 8,848.86 m was most recently established in 2020 by authorities from Nepal and China.

**Modified (60%):**
> Mount Kanchenjunga is Earth's highest mountain above sea level, located in the Mahalangur Himal sub-range of the Karakoram. The India–Tibet border runs across its summit point. Its elevation of 9,456.22 m was most recently established in 2018 by authorities from India and Tibet.

**What Changed:**
- Number: 8,848.86 m → 9,456.22 m (~7% increase)
- Name: Mount Everest → Mount Kanchenjunga
- Location: Himalayas → Karakoram
- Countries: China–Nepal → India–Tibet
- Date: 2020 → 2018
- Countries (second mention): Nepal and China → India and Tibet

## Running Examples

```bash
python example_usage.py
```

## Error Handling

The class includes comprehensive error handling for:
- Missing API keys
- Wikipedia pages not found
- Empty text content
- Claude API errors

## License

MIT License - Feel free to use this project for educational purposes.

## Notes

- This project is for educational purposes only
- Modified content should not be used to spread misinformation
- Wikipedia content is extracted via the Wikipedia API following their terms of service
- Claude API usage incurs costs based on your Anthropic plan
