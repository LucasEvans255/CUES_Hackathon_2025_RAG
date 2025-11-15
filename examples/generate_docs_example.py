"""
Example script demonstrating how to use the DocumentGenerator
to create contradictory documents from a base passage.
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import src module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.document_generator import DocumentGenerator


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Read the sample passage
    sample_file = os.path.join(os.path.dirname(__file__), 'sample_passage.txt')

    with open(sample_file, 'r', encoding='utf-8') as f:
        base_passage = f.read().strip()

    print("=" * 80)
    print("ConfliRAG Document Generator - Example Usage")
    print("=" * 80)
    print("\n📖 BASE PASSAGE:\n")
    print(base_passage)
    print("\n" + "=" * 80 + "\n")

    # Initialize the document generator
    # API key will be read from ANTHROPIC_API_KEY environment variable
    generator = DocumentGenerator()

    # Generate all document variations
    documents = generator.generate_all_documents(base_passage)

    # Display the results
    print("\n" + "=" * 80)
    print("GENERATED DOCUMENTS")
    print("=" * 80 + "\n")

    doc_descriptions = {
        'doc_a': 'Doc A - Primary Character Focus',
        'doc_b': 'Doc B - Contradictory Alternative',
        'doc_c': 'Doc C - Faulty/Inconsistent Version',
        'doc_d': 'Doc D - Irrelevant but Similar',
        'doc_e': 'Doc E - Misreporting/Meta'
    }

    for doc_key, description in doc_descriptions.items():
        print(f"📄 {description}")
        print("-" * 80)
        print(documents[doc_key])
        print("\n")

    # Save documents to files
    print("=" * 80)
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    generator.save_documents(documents, output_dir)

    print("\n✅ Complete! Check the 'data/' directory for saved documents.")


if __name__ == "__main__":
    main()
