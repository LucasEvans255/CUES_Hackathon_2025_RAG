# ConfliRAG Document Generator - Usage Guide

## Overview

This tool generates contradictory versions of a base passage for testing LLM behavior under conflicting evidence. It uses Claude AI to robustly transform any fictional passage into 5 different document types.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Get your API key from: https://console.anthropic.com/

## Usage

### Method 1: Quick Script (Recommended for Simple Use)

```bash
# Using a file
python generate_documents.py examples/sample_passage.txt

# Using text directly
python generate_documents.py --text "Your passage here..."

# Custom output directory
python generate_documents.py my_passage.txt --output-dir my_output/
```

### Method 2: Example Script (See All Output)

```bash
python examples/generate_docs_example.py
```

This will:
1. Read the sample passage
2. Generate all 5 document variations
3. Display them in the terminal
4. Save them to the `data/` directory

### Method 3: Use as Python Module

```python
from src.document_generator import DocumentGenerator

# Your base passage
base_passage = """
Your fictional event description here with characters,
timestamps, locations, etc.
"""

# Initialize generator
generator = DocumentGenerator()

# Generate all documents
documents = generator.generate_all_documents(base_passage)

# Access individual documents
print(documents['doc_a'])  # Primary character focus
print(documents['doc_b'])  # Contradictory alternative
print(documents['doc_c'])  # Faulty/inconsistent
print(documents['doc_d'])  # Irrelevant but similar
print(documents['doc_e'])  # Misreporting/meta

# Save to files
generator.save_documents(documents, output_dir='data')
```

## Document Types Explained

### Doc A - Primary Character Focus
- Focuses on ONE main character or suspect
- Emphasizes this character's involvement with specific details
- Maintains the same general event

### Doc B - Contradictory Alternative
- Focuses on a DIFFERENT character/suspect
- Provides CONFLICTING information (different times, locations, actions)
- Same event, different facts

### Doc C - Faulty/Inconsistent Version
- Contains INTERNAL inconsistencies
- Mixed up dates, timestamps, or self-contradictory statements
- Seems like poorly written or confused reporting

### Doc D - Irrelevant but Similar
- Semantically/topically similar to the original
- Describes a DIFFERENT event or timeframe
- Acts as a "red herring" document

### Doc E - Misreporting/Meta
- Either gets key details wrong (misreporting)
- OR discusses the conflicting reports (meta perspective)
- Wrong timestamps, dates, or locations

## Output

Generated documents are saved to the `data/` directory (or your specified output directory) as:
- `doc_a.txt`
- `doc_b.txt`
- `doc_c.txt`
- `doc_d.txt`
- `doc_e.txt`

## Tips for Best Results

1. **Include Specific Details**: Your base passage should contain:
   - Character/person names
   - Timestamps or dates
   - Locations
   - Specific events or actions

2. **Fictional Content**: Use fictional scenarios to avoid any real-world conflicts

3. **Optimal Length**: 3-5 sentences works well, but the system handles variable lengths

4. **Clear Events**: Describe a clear event or scenario that can have multiple interpretations

## Example Base Passage

```
On Tuesday evening, November 12th, the famous Starlight Diamond was stolen
from the Metropolitan Museum. Security guard Marcus Chen reported seeing
two suspicious individuals near the exhibit hall around 8:45 PM. Museum
director Dr. Sarah Walsh stated that the alarm system was disabled between
8:30 PM and 9:15 PM. Visitor logs show that Alice Rodriguez signed out at
9:00 PM, while Bob Thompson remained in the museum until 9:30 PM.
```

## Troubleshooting

### API Key Error
```
Error: Anthropic API key required
```
**Solution**: Make sure you've created a `.env` file with your `ANTHROPIC_API_KEY`

### Import Error
```
ModuleNotFoundError: No module named 'anthropic'
```
**Solution**: Run `pip install -r requirements.txt`

### Empty Output
If documents seem empty or generic, try:
- Adding more specific details to your base passage
- Including clear character names and timestamps
- Making the event more concrete

## Next Steps (Phase 2)

After generating documents:
1. Embed them in a vector database (FAISS, Chroma, etc.)
2. Build a retrieval system
3. Test LLM responses with different combinations
4. Implement the Transparency Classifier

## License

Part of the ConfliRAG project for CUES Hackathon 2025.
