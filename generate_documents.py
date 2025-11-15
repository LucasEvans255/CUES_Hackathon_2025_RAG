#!/usr/bin/env python3
"""
Simple script to generate contradictory documents from a base passage.

Usage:
    python generate_documents.py <path_to_passage_file>

Or provide passage directly:
    python generate_documents.py --text "Your passage text here"
"""

import sys
import os
import argparse
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.document_generator import DocumentGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Generate contradictory documents from a base passage'
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Path to file containing base passage'
    )
    parser.add_argument(
        '--text',
        '-t',
        help='Provide passage text directly as argument'
    )
    parser.add_argument(
        '--output-dir',
        '-o',
        default='data',
        help='Directory to save generated documents (default: data/)'
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Get base passage from file or argument
    if args.text:
        base_passage = args.text
    elif args.input_file:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            base_passage = f.read().strip()
    else:
        print("Error: Must provide either input file or --text argument")
        print("\nUsage:")
        print("  python generate_documents.py <input_file>")
        print("  python generate_documents.py --text 'Your passage here'")
        sys.exit(1)

    if not base_passage:
        print("Error: Passage is empty")
        sys.exit(1)

    print("=" * 80)
    print("ConfliRAG Document Generator")
    print("=" * 80)
    print("\n📖 BASE PASSAGE:\n")
    print(base_passage)
    print("\n" + "=" * 80 + "\n")

    # Initialize generator and create documents
    try:
        generator = DocumentGenerator()
        documents = generator.generate_all_documents(base_passage)

        # Save documents
        print("\n" + "=" * 80)
        generator.save_documents(documents, args.output_dir)
        print(f"\n✅ Complete! Documents saved to '{args.output_dir}/' directory")

    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have set ANTHROPIC_API_KEY in your .env file")
        print("See .env.example for reference")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
