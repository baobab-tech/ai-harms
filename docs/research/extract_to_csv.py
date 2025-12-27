#!/usr/bin/env python3
"""Extract research entries from markdown files into CSV format."""
import re
import csv
import os
from pathlib import Path

def extract_topic_from_filename(filename):
    """Convert filename like '01-ai-psychosis.md' to 'AI Psychosis'."""
    # Remove number prefix and extension
    name = re.sub(r'^\d+-', '', filename.replace('.md', ''))
    # Convert kebab-case to title case, with special handling for 'ai'
    words = []
    for word in name.split('-'):
        if word.lower() == 'ai':
            words.append('AI')
        else:
            words.append(word.capitalize())
    return ' '.join(words)

def parse_md_file(filepath):
    """Parse a markdown file and extract all research entries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    topic = extract_topic_from_filename(os.path.basename(filepath))
    entries = []

    # Find all bullet points (lines starting with -)
    # Pattern matches: - description **Reference:** or **Source:** ... [Link](url) or [Source Name](url)
    bullet_pattern = re.compile(
        r'^- (.+?)(?:\*\*Reference:\*\*|\*\*Source:\*\*)\s*(.+?)$',
        re.MULTILINE | re.DOTALL
    )

    # Split content by bullet points for better parsing
    lines = content.split('\n')
    current_entry = []

    for line in lines:
        if line.startswith('- '):
            if current_entry:
                # Process previous entry
                entry_text = ' '.join(current_entry)
                parsed = parse_entry(entry_text, topic)
                if parsed:
                    entries.append(parsed)
            current_entry = [line[2:]]  # Remove '- ' prefix
        elif current_entry and line.strip() and not line.startswith('#'):
            current_entry.append(line.strip())

    # Don't forget the last entry
    if current_entry:
        entry_text = ' '.join(current_entry)
        parsed = parse_entry(entry_text, topic)
        if parsed:
            entries.append(parsed)

    return entries

def parse_entry(text, topic):
    """Parse a single entry and extract fields."""
    # Skip non-research entries (like risk factors, research gaps without refs)
    if '**Reference:**' not in text and '**Source:**' not in text:
        return None

    # Split by Reference: or Source:
    is_source = '**Source:**' in text
    if '**Reference:**' in text:
        parts = text.split('**Reference:**', 1)
    else:
        parts = text.split('**Source:**', 1)

    oneline = parts[0].strip()
    ref_section = parts[1].strip() if len(parts) > 1 else ''

    # Extract URL and link text first (we'll need it)
    url_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', ref_section)
    url = url_match.group(2) if url_match else ''
    link_text = url_match.group(1) if url_match else ''

    title = ''
    source = ''

    if is_source:
        # For **Source:** entries, format is [Title - Publication](url)
        if link_text and ' - ' in link_text:
            parts_link = link_text.split(' - ', 1)
            title = parts_link[0].strip()
            source = parts_link[1].strip()
        elif link_text:
            title = link_text
    else:
        # For **Reference:** entries, title is in quotes, source in italics
        title_match = re.search(r'"([^"]+)"', ref_section)
        if title_match:
            title = title_match.group(1)

        # Extract source from italics (journal name)
        italic_match = re.search(r'\*([^*]+)\*', ref_section)
        if italic_match:
            source = italic_match.group(1)

    # Fallbacks if still empty
    if not title:
        # Try quotes anywhere
        title_match = re.search(r'"([^"]+)"', ref_section)
        if title_match:
            title = title_match.group(1)
        elif link_text and link_text != 'Link':
            title = link_text.split(' - ')[0] if ' - ' in link_text else link_text
        else:
            # Last resort: use beginning of ref section
            title_match = re.search(r'^([A-Z][^.(]+)', ref_section)
            title = title_match.group(1).strip() if title_match else "Untitled"

    if not source:
        # Try italics
        italic_match = re.search(r'\*([^*]+)\*', ref_section)
        if italic_match:
            source = italic_match.group(1)
        elif link_text and link_text != 'Link':
            # Use link text or part after dash
            source = link_text.split(' - ')[-1] if ' - ' in link_text else link_text
        else:
            # Extract author/publication from start
            source_match = re.search(r'^([A-Z][^(]+?)(?:\(|\.)', ref_section)
            source = source_match.group(1).strip() if source_match else ''

    return {
        'topic': topic,
        'title': title[:500],  # Truncate long titles
        'oneline': oneline[:1000],  # Truncate long descriptions
        'source': source[:200],
        'url': url
    }

def process_all_files(research_dir):
    """Process all MD files except all.md."""
    research_path = Path(research_dir)

    for md_file in sorted(research_path.glob('*.md')):
        if md_file.name == 'all.md':
            continue

        print(f"Processing: {md_file.name}")
        entries = parse_md_file(md_file)

        if entries:
            csv_filename = md_file.stem + '.csv'
            csv_path = research_path / csv_filename

            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['topic', 'title', 'oneline', 'source', 'url'])
                writer.writeheader()
                writer.writerows(entries)

            print(f"  -> Created {csv_filename} with {len(entries)} entries")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    process_all_files(script_dir)
    print("\nDone! CSV files created for each markdown file.")
