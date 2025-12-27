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

- **Sources**: arXiv and OpenAlex academic databases
- **Agent**: Claude with web search and fetch capabilities
- **Output**: Structured markdown documents with references, converted to CSV

## Usage

To extract research entries to CSV:

```bash
cd docs/research
python3 extract_to_csv.py
```

## Acknowledgments

Thank you to arXiv for use of its open access interoperability.
