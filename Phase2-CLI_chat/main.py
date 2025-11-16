#!/usr/bin/env python3
"""
Main entry point for the Claude Chat CLI application.

This application allows users to:
- Create new chat sessions with Claude AI
- Add context files to the conversation
- Save chat history to text files
- Track all chats in a CSV index file
- Recreate and display saved chats with context
- Batch process prompts from CSV files

Usage:
    python main.py                      # Start interactive CLI (default CSV: chats_index.csv)
    python main.py -f <csv>             # Start interactive CLI with custom CSV file
    python main.py -f <csv> -a <idx>    # Display chat at index from CSV
    python main.py -i <input.csv> -o <output.csv>  # Batch process prompts from CSV
"""

import argparse
from cli import CLI
from chat_manager import ChatManager
from chat_recreator import ChatRecreator
from batch_processor import BatchProcessor


def main():
    """
    Main function to run the CLI application.
    """
    parser = argparse.ArgumentParser(
        description="Claude Chat CLI - Interactive chat with file context support"
    )
    parser.add_argument(
        '-f',
        '--file',
        type=str,
        help='Path to the CSV file containing chat index'
    )
    parser.add_argument(
        '-a',
        '--at',
        type=int,
        help='Index of the chat to display from the CSV (0-based)'
    )
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='Input CSV file for batch processing (format: prompt, file1, file2, ...)'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='Output CSV file for batch processing results'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='claude-sonnet-4-5-20250929',
        help='Claude model to use for batch processing (default: claude-sonnet-4-5-20250929)'
    )
    parser.add_argument(
        '--max-tokens',
        type=int,
        default=4096,
        help='Maximum tokens for responses in batch processing (default: 4096)'
    )
    parser.add_argument(
        '--temperature',
        type=float,
        default=1.0,
        help='Temperature for response generation in batch processing (default: 1.0)'
    )

    args = parser.parse_args()

    # Check if we're in batch processing mode
    if args.input is not None or args.output is not None:
        if args.input is None or args.output is None:
            print("Error: Both -i and -o arguments must be provided for batch processing")
            parser.print_help()
            return
        batch_process(args.input, args.output, args.model, args.max_tokens, args.temperature)
    # Check if we're in display mode
    elif args.at is not None:
        if args.file is None:
            print("Error: -f argument must be provided when using -a")
            parser.print_help()
            return
        display_chat(args.file, args.at)
    else:
        # Run interactive CLI
        if args.file is None:
            cli = CLI()
        else:
            cli = CLI(csv_filepath=args.file)
        cli.run()


def batch_process(input_filepath: str, output_filepath: str, model: str, max_tokens: int, temperature: float):
    """
    Batch process prompts from a CSV file and save responses to another CSV.

    Args:
        input_filepath: Path to input CSV file
        output_filepath: Path to output CSV file
        model: Claude model to use
        max_tokens: Maximum tokens for responses
        temperature: Temperature for response generation
    """
    try:
        processor = BatchProcessor(model=model, max_tokens=max_tokens, temperature=temperature)
        processor.run(input_filepath, output_filepath)
    except Exception as e:
        print(f"Error during batch processing: {e}")


def display_chat(csv_filepath: str, index: int):
    """
    Display a chat from the CSV file at the specified index.

    Args:
        csv_filepath: Path to the CSV file.
        index: Index of the chat to display.
    """
    try:
        # Get the chat info from CSV
        manager = ChatManager(csv_filepath)
        chat_info = manager.get_chat_by_index(index)

        chat_filepath = chat_info['chat_filepath']
        context_files = chat_info['context_files']

        print(f"Loading chat from index {index}...")
        print(f"Chat file: {chat_filepath}")
        print(f"Context files: {', '.join(context_files) if context_files else 'None'}")
        print("\n" + "=" * 80 + "\n")

        # Recreate and display the chat
        ChatRecreator.recreate_chat(chat_filepath, context_files)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except IndexError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()