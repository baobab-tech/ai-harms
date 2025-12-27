# LLM Harm Research

AI-powered deep research repository using Claude's agentic methodology.

## Overview

This repository contains research outputs generated using Claude with sub-agents to explore various topics related to potential harms from large language models and AI systems.

## Structure

```
docs/
├── arxiv-api.md          # arXiv API reference
├── openalex-api.md       # OpenAlex API reference
└── research/
    ├── 01-ai-psychosis.md
    ├── 02-parasocial-attachment.md
    ├── ...
    ├── 12-radicalization.md
    ├── all.md             # Combined research
    ├── *.csv              # Extracted data
    └── extract_to_csv.py  # Utility script
```

## Methodology

Research was generated using [Claude Code](https://claude.ai/code) with parallel sub-agents. Each topic was researched independently and output to its own markdown file.

### Running the Research

1. Install Claude Code CLI
2. Run with a prompt like:

```
For each of the following topics, spawn a sub-agent to research it independently.
Use arXiv and OpenAlex APIs to find academic papers and sources.
Output each topic to its own numbered markdown file in docs/research/.

Topics:
1. AI-induced psychosis and reality distortion
2. Parasocial attachment to AI systems
3. Relationship breakdown from AI companions
4. Self-harm and suicide risks
5. AI addiction patterns
6. Identity confusion and derealization
7. Manipulation and deception by AI
8. Youth-specific harms
9. Grief exploitation by AI
10. Social isolation effects
11. Sexual and romantic harms
12. Radicalization risks

For each topic, find relevant research papers, case studies, and documented incidents.
Include proper citations with URLs.
```

### Sources

- **arXiv**: Academic preprints via API (see `docs/arxiv-api.md`)
- **OpenAlex**: Scholarly works database (see `docs/openalex-api.md`)

## Usage

To extract research entries to CSV:

```bash
cd docs/research
python3 extract_to_csv.py
```

## Acknowledgments

Thank you to arXiv for use of its open access interoperability.
