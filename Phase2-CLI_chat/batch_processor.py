import csv
from typing import List, Dict
from claude_chat import ClaudeChat


class BatchProcessor:
    """
    Batch processor for handling CSV-based prompt processing with Claude.

    Reads prompts and context files from a CSV, processes them using ClaudeChat,
    and writes the responses to an output CSV.
    """

    def __init__(self, model: str = 'claude-sonnet-4-5-20250929',
                 max_tokens: int = 4096,
                 temperature: float = 1.0):
        """
        Initialize the batch processor.

        Args:
            model: Claude model to use
            max_tokens: Maximum tokens for response
            temperature: Temperature for response generation
        """
        self.claude = ClaudeChat(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )

    def read_input_csv(self, input_filepath: str) -> List[Dict[str, any]]:
        """
        Read input CSV file and parse prompts with their context files.

        Args:
            input_filepath: Path to input CSV file

        Returns:
            List of dictionaries with 'prompt' and 'context_files' keys
        """
        rows = []

        with open(input_filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for row_num, row in enumerate(reader, start=1):
                if not row:  # Skip empty rows
                    continue

                prompt = row[0].strip() if row else ""

                if not prompt:
                    print(f"Warning: Row {row_num} has empty prompt. Skipping.")
                    continue

                # Get context files (all columns after the prompt)
                context_files = [filepath.strip() for filepath in row[1:] if filepath.strip()] if len(row) > 1 else []

                rows.append({
                    'prompt': prompt,
                    'context_files': context_files
                })

        print(f"Successfully loaded {len(rows)} prompts from {input_filepath}\n")
        return rows

    def process_prompts(self, rows: List[Dict[str, any]]) -> List[Dict[str, str]]:
        """
        Process each prompt with its context files using ClaudeChat.

        Args:
            rows: List of dictionaries with 'prompt' and 'context_files'

        Returns:
            List of dictionaries with 'prompt', 'context_filepaths', and 'response'
        """
        results = []

        for idx, row in enumerate(rows, start=1):
            prompt = row['prompt']
            context_files = row['context_files']

            print(f"[{idx}/{len(rows)}] Processing prompt: {prompt[:60]}...")
            if context_files:
                print(f"  Context files: {', '.join(context_files)}")
            else:
                print(f"  No context files provided")

            try:
                # Use ClaudeChat.ask() with or without context files
                response = self.claude.ask(prompt, filepaths=context_files if context_files else None)

                # Join context files with semicolons for CSV output
                context_filepaths_str = ';'.join(context_files) if context_files else ''

                results.append({
                    'prompt': prompt,
                    'context_filepaths': context_filepaths_str,
                    'response': response
                })

                print(f"  ✓ Response received ({len(response)} chars)\n")

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                print(f"  ✗ {error_msg}\n")
                results.append({
                    'prompt': prompt,
                    'context_filepaths': ';'.join(context_files) if context_files else '',
                    'response': error_msg
                })

        return results

    def write_output_csv(self, output_filepath: str, results: List[Dict[str, str]]):
        """
        Write results to output CSV file.

        Args:
            output_filepath: Path to output CSV file
            results: List of dictionaries with 'prompt', 'context_filepaths', and 'response'
        """
        with open(output_filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(['prompt', 'context_filepaths', 'response'])

            # Write data rows
            for result in results:
                writer.writerow([
                    result['prompt'],
                    result['context_filepaths'],
                    result['response']
                ])

        print(f"✓ Successfully wrote {len(results)} results to {output_filepath}")

    def run(self, input_filepath: str, output_filepath: str):
        """
        Run the batch processing pipeline.

        Args:
            input_filepath: Path to input CSV file
            output_filepath: Path to output CSV file
        """
        print("=" * 80)
        print("Claude Batch Processor")
        print("=" * 80)

        # Read input CSV
        rows = self.read_input_csv(input_filepath)

        if not rows:
            print("No valid prompts found in input file.")
            return

        # Process prompts
        results = self.process_prompts(rows)

        # Write output CSV
        self.write_output_csv(output_filepath, results)

        print("=" * 80)
        print("Batch processing complete!")
        print("=" * 80)
