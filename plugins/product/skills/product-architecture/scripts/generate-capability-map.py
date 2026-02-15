#!/usr/bin/env python3
"""
Generate an SVG visualization from a capability map markdown file.

Usage:
    python generate-capability-map.py [--input INPUT_FILE] [--output OUTPUT_FILE]

By default, looks for .product/capability-map.md in the current directory
and outputs to .product/capability-map.svg

Options:
    --input     Input markdown file path (default: .product/capability-map.md)
    --output    Output SVG file path (default: .product/capability-map.svg)
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional


# SVG styling constants
DOMAIN_WIDTH = 300
DOMAIN_MIN_HEIGHT = 200
GROUP_SPACING = 15
CAPABILITY_HEIGHT = 25
DOMAIN_PADDING = 20
DOMAIN_SPACING_H = 30
DOMAIN_SPACING_V = 30
TITLE_HEIGHT = 40


def parse_simple_yaml_layout(yaml_text: str) -> Optional[Dict[str, Any]]:
    """
    Parse a simple YAML layout structure without external dependencies.

    Expected structure:
    layout:
      row:
        - Domain Name
        - column:
            - Another Domain
            - Yet Another Domain
    """
    if 'layout:' not in yaml_text:
        return None

    layout = {'row': []}
    lines = yaml_text.split('\n')

    in_layout = False
    in_row = False
    in_column = False
    current_column = []
    indent_level = 0

    for line in lines:
        stripped = line.strip()

        if stripped == 'layout:':
            in_layout = True
            continue

        if not in_layout:
            continue

        # Check indentation
        if line and not line[0].isspace():
            # New top-level key, exit layout parsing
            break

        if '  row:' in line or 'row:' in line:
            in_row = True
            in_column = False
            continue

        if in_row:
            if '    - column:' in line or '  - column:' in line:
                # Start of column
                in_column = True
                current_column = []
                continue

            if in_column:
                if line.startswith('      - ') or line.startswith('        - '):
                    # Item in column
                    item = stripped[2:].strip()
                    current_column.append(item)
                elif stripped.startswith('- '):
                    # End of column, start of new row item
                    if current_column:
                        layout['row'].append({'column': current_column})
                        current_column = []
                    in_column = False
                    item = stripped[2:].strip()
                    layout['row'].append(item)
            else:
                if stripped.startswith('- '):
                    # Direct row item
                    item = stripped[2:].strip()
                    if item and item != 'column:':
                        layout['row'].append(item)

    # Add any remaining column
    if current_column:
        layout['row'].append({'column': current_column})

    return layout if layout['row'] else None


def parse_capability_map(content: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Parse capability map markdown and extract layout and content.

    Returns:
        Tuple of (layout_dict, domains_dict)
    """
    # Split frontmatter and content
    parts = content.split('---')
    if len(parts) >= 3:
        frontmatter = parts[1].strip()
        markdown_content = '---'.join(parts[2:]).strip()
    else:
        frontmatter = ""
        markdown_content = content

    # Parse YAML frontmatter
    layout = parse_simple_yaml_layout(frontmatter) if frontmatter else None
    if not layout:
        layout = {}

    # Parse markdown content
    domains = {}
    current_domain = None
    current_group = None

    lines = markdown_content.split('\n')

    for line in lines:
        stripped = line.strip()

        # Domain header (## Domain Name)
        if stripped.startswith('## ') and not stripped.startswith('###'):
            domain_name = stripped[3:].strip()
            if domain_name and domain_name != 'Capability Map':
                current_domain = domain_name
                domains[current_domain] = {}
                current_group = None

        # Capability group header (### Group Name)
        elif stripped.startswith('### '):
            if current_domain:
                # Extract group name and owner
                group_text = stripped[4:].strip()

                # Check for owner tag in backticks or brackets
                owner = None
                group_name = group_text

                # Match `[owner: team-name]`
                owner_match = re.search(r'`\[owner:\s*([^\]]+)\]`', group_text)
                if owner_match:
                    owner = owner_match.group(1).strip()
                    group_name = group_text[:owner_match.start()].strip()
                else:
                    # Match [owner: team-name] without backticks
                    owner_match = re.search(r'\[owner:\s*([^\]]+)\]', group_text)
                    if owner_match:
                        owner = owner_match.group(1).strip()
                        group_name = group_text[:owner_match.start()].strip()

                current_group = group_name
                domains[current_domain][current_group] = {
                    'owner': owner,
                    'capabilities': []
                }

        # Capability item (- **Capability Name**: Description)
        elif stripped.startswith('- **') and current_domain and current_group:
            # Extract capability name and description
            cap_match = re.match(r'-\s*\*\*([^*]+)\*\*:?\s*(.*)', stripped)
            if cap_match:
                cap_name = cap_match.group(1).strip()
                cap_desc = cap_match.group(2).strip()
                domains[current_domain][current_group]['capabilities'].append({
                    'name': cap_name,
                    'description': cap_desc
                })

    return layout, domains


def calculate_domain_height(domain_data: Dict) -> int:
    """Calculate the height needed for a domain box."""
    height = TITLE_HEIGHT + DOMAIN_PADDING * 2

    for group_name, group_data in domain_data.items():
        # Group header
        height += 30

        # Capabilities
        num_capabilities = len(group_data['capabilities'])
        if num_capabilities > 0:
            height += num_capabilities * CAPABILITY_HEIGHT
        else:
            height += 20  # Empty group

        # Spacing between groups
        height += GROUP_SPACING

    return max(height, DOMAIN_MIN_HEIGHT)


def flatten_layout(layout: Dict, domains: Dict[str, Any]) -> List[List[str]]:
    """
    Convert layout structure to a 2D grid of domain names.

    Returns:
        List of rows, where each row is a list of domain names
    """
    if not layout or 'row' not in layout:
        # Default layout: single row with all domains
        return [list(domains.keys())]

    row_items = layout['row']
    grid = []

    max_col_height = 1

    # First pass: determine max column height
    for item in row_items:
        if isinstance(item, dict) and 'column' in item:
            col_height = len(item['column'])
            max_col_height = max(max_col_height, col_height)

    # Second pass: build grid
    for row_idx in range(max_col_height):
        row = []
        for item in row_items:
            if isinstance(item, str):
                # Single domain
                if row_idx == 0:
                    row.append(item)
                else:
                    row.append(None)  # Empty cell
            elif isinstance(item, dict) and 'column' in item:
                # Column of domains
                col_domains = item['column']
                if row_idx < len(col_domains):
                    row.append(col_domains[row_idx])
                else:
                    row.append(None)  # Empty cell
        grid.append(row)

    return grid


def generate_svg(layout: Dict, domains: Dict[str, Any]) -> str:
    """Generate SVG markup for the capability map."""

    # Flatten layout to grid
    grid = flatten_layout(layout, domains)

    # Calculate dimensions for each domain
    domain_heights = {}
    for domain_name, domain_data in domains.items():
        domain_heights[domain_name] = calculate_domain_height(domain_data)

    # Calculate row heights (max height in each row)
    row_heights = []
    for row in grid:
        max_height = DOMAIN_MIN_HEIGHT
        for domain_name in row:
            if domain_name and domain_name in domain_heights:
                max_height = max(max_height, domain_heights[domain_name])
        row_heights.append(max_height)

    # Calculate total dimensions
    num_cols = max(len(row) for row in grid) if grid else 1
    total_width = num_cols * DOMAIN_WIDTH + (num_cols + 1) * DOMAIN_SPACING_H
    total_height = sum(row_heights) + (len(row_heights) + 1) * DOMAIN_SPACING_V

    # Start SVG
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} {total_height}" width="{total_width}" height="{total_height}">',
        '<defs>',
        '<style>',
        '.domain { fill: #f8f9fa; stroke: #dee2e6; stroke-width: 2; }',
        '.domain-title { font-family: sans-serif; font-size: 18px; font-weight: bold; fill: #212529; }',
        '.group-title { font-family: sans-serif; font-size: 14px; font-weight: 600; fill: #495057; }',
        '.owner { font-family: sans-serif; font-size: 11px; fill: #6c757d; }',
        '.capability { font-family: sans-serif; font-size: 12px; fill: #212529; }',
        '.group-box { fill: #ffffff; stroke: #adb5bd; stroke-width: 1; }',
        '</style>',
        '</defs>',
    ]

    # Render domains
    y_offset = DOMAIN_SPACING_V

    for row_idx, row in enumerate(grid):
        x_offset = DOMAIN_SPACING_H
        row_height = row_heights[row_idx]

        for col_idx, domain_name in enumerate(row):
            if domain_name and domain_name in domains:
                domain_data = domains[domain_name]
                domain_height = domain_heights[domain_name]

                # Draw domain box
                svg_lines.append(
                    f'<rect class="domain" x="{x_offset}" y="{y_offset}" '
                    f'width="{DOMAIN_WIDTH}" height="{domain_height}" rx="8"/>'
                )

                # Draw domain title
                title_y = y_offset + 30
                svg_lines.append(
                    f'<text class="domain-title" x="{x_offset + DOMAIN_WIDTH/2}" '
                    f'y="{title_y}" text-anchor="middle">{escape_xml(domain_name)}</text>'
                )

                # Draw capability groups
                group_y = y_offset + TITLE_HEIGHT + DOMAIN_PADDING

                for group_name, group_data in domain_data.items():
                    group_height = 30 + len(group_data['capabilities']) * CAPABILITY_HEIGHT
                    if len(group_data['capabilities']) == 0:
                        group_height = 30 + 20

                    # Group box
                    svg_lines.append(
                        f'<rect class="group-box" x="{x_offset + 10}" y="{group_y}" '
                        f'width="{DOMAIN_WIDTH - 20}" height="{group_height}" rx="4"/>'
                    )

                    # Group title
                    svg_lines.append(
                        f'<text class="group-title" x="{x_offset + 20}" '
                        f'y="{group_y + 20}">{escape_xml(group_name)}</text>'
                    )

                    # Owner tag
                    if group_data['owner']:
                        svg_lines.append(
                            f'<text class="owner" x="{x_offset + DOMAIN_WIDTH - 20}" '
                            f'y="{group_y + 20}" text-anchor="end">[{escape_xml(group_data["owner"])}]</text>'
                        )

                    # Capabilities
                    cap_y = group_y + 35
                    for capability in group_data['capabilities']:
                        svg_lines.append(
                            f'<text class="capability" x="{x_offset + 20}" '
                            f'y="{cap_y}">• {escape_xml(capability["name"])}</text>'
                        )
                        cap_y += CAPABILITY_HEIGHT

                    group_y += group_height + GROUP_SPACING

            x_offset += DOMAIN_WIDTH + DOMAIN_SPACING_H

        y_offset += row_height + DOMAIN_SPACING_V

    svg_lines.append('</svg>')

    return '\n'.join(svg_lines)


def escape_xml(text: str) -> str:
    """Escape XML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))


def main():
    parser = argparse.ArgumentParser(
        description='Generate an SVG visualization from capability map markdown',
        epilog='By default, looks for .product/capability-map.md in the current directory'
    )
    parser.add_argument(
        '--input',
        default='.product/capability-map.md',
        help='Input markdown file path (default: .product/capability-map.md)'
    )
    parser.add_argument(
        '--output',
        default='.product/capability-map.svg',
        help='Output SVG file path (default: .product/capability-map.svg)'
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
    layout, domains = parse_capability_map(content)
    svg_content = generate_svg(layout, domains)

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print(f"Generated capability map SVG: {output_file}")
    print(f"Found {len(domains)} domains with {sum(len(d) for d in domains.values())} capability groups")

    return 0


if __name__ == '__main__':
    exit(main())
