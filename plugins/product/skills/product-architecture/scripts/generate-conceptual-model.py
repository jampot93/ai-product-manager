#!/usr/bin/env python3
"""
Generate a Mermaid entity relationship diagram from a conceptual data model markdown file.

Usage:
    python generate-conceptual-model.py [--input INPUT_FILE] [--output OUTPUT_FILE]

By default, looks for .product/conceptual-data-model.md in the current directory
and outputs to .product/conceptual-data-model.mmd

Options:
    --input     Input markdown file path (default: .product/conceptual-data-model.md)
    --output    Output Mermaid file path (default: .product/conceptual-data-model.mmd)
"""

import re
import argparse
from pathlib import Path


def parse_cardinality(cardinality_text):
    """
    Convert cardinality text to Mermaid ER notation.

    Format: "target-cardinality to source-cardinality (relationship-name)"
    Example: "one-or-many to one (owns)"

    The cardinality reads target-to-source: "one-or-many to one" means
    "one-or-many of them (target) relate to one of me (source)"

    Mermaid notation: markers differ by position (left vs right of --)
    In each marker: innermost char = minimum, outermost char = maximum
    """
    # Left side markers (before --)
    left_card_map = {
        'one': '||',
        'zero-or-one': '|o',
        'zero-or-many': '}o',
        'one-or-many': '}|',
        'many': '}|'
    }

    # Right side markers (after --)
    right_card_map = {
        'one': '||',
        'zero-or-one': 'o|',
        'zero-or-many': 'o{',
        'one-or-many': '|{',
        'many': '|{'
    }

    # Parse the format "target to source (relationship)"
    match = re.match(r'([\w-]+)\s+to\s+([\w-]+)\s*\(([^)]+)\)', cardinality_text.strip())
    if not match:
        return None, None, None

    target_card, source_card, relationship = match.groups()

    # Convert to Mermaid notation
    # In Mermaid: ENTITY1 left_symbol--right_symbol ENTITY2
    # left_symbol is for source (ENTITY1), right_symbol is for target (ENTITY2)
    source_symbol = left_card_map.get(source_card.lower(), '||')
    target_symbol = right_card_map.get(target_card.lower(), '||')

    return source_symbol, target_symbol, relationship.strip()


def parse_conceptual_model(content):
    """Parse the conceptual data model markdown and extract entities and relationships."""

    domains = {}
    current_domain = None
    current_entity = None
    in_relationships = False

    lines = content.split('\n')

    for line in lines:
        stripped = line.strip()

        # Skip frontmatter
        if stripped == '---':
            continue

        # Domain header (## Domain Name)
        if stripped.startswith('## ') and not stripped.startswith('###'):
            current_domain = stripped[3:].strip()
            if current_domain != 'Conceptual Data Model':  # Skip main title
                domains[current_domain] = {}
                current_entity = None
                in_relationships = False

        # Entity header (bold text like **Entity Name**)
        elif stripped.startswith('**') and stripped.endswith('**'):
            entity_name = stripped[2:-2].strip()
            if current_domain and current_domain in domains:
                domains[current_domain][entity_name] = []
                current_entity = entity_name
                in_relationships = False

        # Relationship line (  - Target Entity: cardinality) - CHECK THIS FIRST
        elif in_relationships and current_entity and (line.startswith('  - ') or line.startswith('    - ')):
            rel_text = line.lstrip(' -').strip()
            if ':' in rel_text:
                target_entity, cardinality = rel_text.split(':', 1)
                domains[current_domain][current_entity].append({
                    'target': target_entity.strip(),
                    'cardinality': cardinality.strip()
                })

        # Relationships section marker
        elif stripped == '- Relationships:':
            in_relationships = True

        # End of relationships section (non-indented list items with colons)
        elif line.startswith('- ') and not line.startswith('  -'):
            # This is a new section (Definition, Constraints, etc.)
            in_relationships = False

    return domains


def generate_mermaid(domains):
    """Generate a Mermaid ER diagram from parsed domains."""

    lines = ['erDiagram']
    lines.append('')

    # Process each domain
    for domain_name, entities in domains.items():
        lines.append(f'    %% {domain_name}')
        lines.append('')

        # Define relationships
        for entity_name, relationships in entities.items():
            entity_id = entity_name.replace(' ', '_').replace('-', '_')

            for rel in relationships:
                target_id = rel['target'].replace(' ', '_').replace('-', '_')
                source_symbol, target_symbol, rel_name = parse_cardinality(rel['cardinality'])

                if source_symbol and target_symbol and rel_name:
                    # Format: SOURCE source_symbol--target_symbol TARGET : "relationship"
                    lines.append(f'    {entity_id} {source_symbol}--{target_symbol} {target_id} : "{rel_name}"')

        lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate a Mermaid ER diagram from conceptual data model markdown',
        epilog='By default, looks for .product/conceptual-data-model.md in the current directory'
    )
    parser.add_argument(
        '--input',
        default='.product/conceptual-data-model.md',
        help='Input markdown file path (default: .product/conceptual-data-model.md)'
    )
    parser.add_argument(
        '--output',
        default='.product/conceptual-data-model.mmd',
        help='Output Mermaid file path (default: .product/conceptual-data-model.mmd)'
    )

    args = parser.parse_args()

    # Determine paths (relative to current working directory)
    input_file = Path(args.input).resolve()
    output_file = Path(args.output).resolve()

    # Read input file
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return 1

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse and generate
    domains = parse_conceptual_model(content)
    mermaid_diagram = generate_mermaid(domains)

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(mermaid_diagram)

    print(f"Generated Mermaid diagram: {output_file}")
    print(f"Found {sum(len(entities) for entities in domains.values())} entities across {len(domains)} domains")

    return 0


if __name__ == '__main__':
    exit(main())
