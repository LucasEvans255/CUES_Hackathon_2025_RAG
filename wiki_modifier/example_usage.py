"""
Example usage of the WikipediaModifier class
"""

from wikipedia_modifier import WikipediaModifier


def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===\n")

    # Initialize with default 20% modification
    modifier = WikipediaModifier()

    # Process a topic
    result = modifier.process("World War II")

    print(f"Topic: {result['topic']}")
    print(f"Wikipedia Page: {result['wikipedia_page']}")
    print(f"Modification: {result['modification_percentage']}%\n")
    print("Original text (first 1000 chars):")
    print(result['original_text'][:5000])
    print("\n" + "="*80 + "\n")
    print("Modified text (first 500 chars):")
    print(result['modified_text'][:5000])
    print("\n")
    return result['modified_text']

def create_fake_text(topic: str, percentage=60.0, output_filepath='output.txt'):
    modifier = WikipediaModifier()

    result = modifier.process(topic)

    return open(output_filepath, 'w').write(result['modified_text'])


def example_custom_modification():
    """Example with custom modification percentage"""
    print("=== Custom Modification Percentage Example ===\n")

    # Initialize with 50% modification
    modifier = WikipediaModifier(modification_percentage=50.0)

    # Extract textp
    topic = "Mount Everest"
    modifier.extract_text(topic)

    # Modify with custom percentage
    modified = modifier.modify_facts(modification_percentage=75.0)

    print(f"Topic: {topic}")
    print(f"Modified with: 75% variation\n")
    print("Modified text (first 1000 chars):")
    print(modified[:1000])
    print("\n")


def example_step_by_step():
    """Example showing step-by-step process"""
    print("=== Step-by-Step Example ===\n")

    # Initialize
    modifier = WikipediaModifier(modification_percentage=30.0)

    # Step 1: Search for Wikipedia page
    topic = "Python programming language"
    page_title = modifier.search_wikipedia(topic)
    print(f"1. Found Wikipedia page: {page_title}")

    # Step 2: Extract text
    text = modifier.extract_text(topic)
    print(f"2. Extracted {len(text)} characters of text")

    # Step 3: Modify facts
    modified = modifier.modify_facts()
    print(f"3. Modified text: {len(modified)} characters")

    # Step 4: Get comparison
    comparison = modifier.get_comparison()
    print(f"\n4. Comparison ready:")
    print(f"   - Original length: {len(comparison['original'])}")
    print(f"   - Modified length: {len(comparison['modified'])}")
    print(f"   - Modification %: {comparison['modification_percentage']}%")
    print("\n")


def example_multiple_modifications():
    """Example showing different modification levels on same text"""
    print("=== Multiple Modification Levels Example ===\n")

    modifier = WikipediaModifier()
    topic = "Eiffel Tower"

    # Extract once
    modifier.extract_text(topic)
    print(f"Topic: {topic}\n")

    # Try different modification percentages
    for percentage in [10, 50, 100]:
        modified = modifier.modify_facts(modification_percentage=percentage)
        print(f"Modified with {percentage}% (first 300 chars):")
        print(modified[:300])
        print("\n" + "-"*80 + "\n")


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("WIKIPEDIA MODIFIER - EXAMPLES")
    print("="*80 + "\n")

    try:
        # Run basic example
        example_basic_usage()

        # Uncomment to run other examples:
        # example_custom_modification()
        # example_step_by_step()
        # example_multiple_modifications()

    except ValueError as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Install requirements: pip install -r requirements.txt")
        print("2. Create .env file with your ANTHROPIC_API_KEY")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
