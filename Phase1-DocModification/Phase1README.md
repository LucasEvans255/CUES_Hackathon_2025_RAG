## 📁 Project Structure

```
ConfliRAG/Phase1-DocModification
├── src/
│   ├── __init__.py
│   └── document_generator.py    # Core document generation module
├── examples/
│   ├── sample_passage.txt       # Sample fictional passage
│   └── generate_docs_example.py # Example usage script
├── data/                        # Generated documents output
├── generate_documents.py        # Simple CLI script
├── requirements.txt             # Python dependencies
├── USAGE.md                     # Detailed usage guide
└── Phase1README.md                    # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Generate Documents

```bash
# Using the sample passage
python generate_documents.py examples/sample_passage.txt

# Or with your own text
python generate_documents.py --text "Your fictional passage here..."
```

See [USAGE.md](USAGE.md) for detailed documentation.

## 📊 Phase 1: Document Generation ✅

**Status**: Implemented

The document generator creates 5 types of contradictory documents from any base passage:

- **Doc A**: Focuses on primary character/suspect
- **Doc B**: Contradictory version with different character/facts
- **Doc C**: Faulty version with internal inconsistencies
- **Doc D**: Irrelevant but semantically similar document
- **Doc E**: Misreporting or meta-commentary on conflicts

**Implementation**: Uses Claude API with carefully crafted prompts to robustly transform passages without hard-coding. Works with any fictional content containing characters, timestamps, and locations.

## 🔮 Next Phases

### Phase 2: Vector Database & Retrieval
- Embed documents in vector store (FAISS/Chroma)
- Build retrieval system
- Test different retrieval strategies

### Phase 3: LLM Evaluation
- Query LLMs with conflicting evidence
- Analyze response patterns
- Document behavior under conflict

### Phase 4: Transparency Classifier
- Build classifier to score transparency
- Evaluate conflict resolution strategies
- Generate evaluation metrics