# Orthanc - Digital Twin Architecture Documentation

## Project Goal
Orthanc is a local, autonomous Digital Twin designed to replicate the user's workflow. It uses a hybrid memory system (SQL + Vector) and interacts with the OS via MCP (Model Context Protocol).

## Architecture Overview

### 1. The Brain (Memory)
- **`db_manager.py`**: The core logic for data persistence.
  - **Structured Data (SQLite)**: Stores strict relationships (Contacts, Interactions logs).
  - **Semantic Data (ChromaDB)**: Stores embeddings for "fuzzy" search (memories, context, style).
  - **File System**: Markdown files for daily journals (`diary.md`).

### 2. The Hands (MCP Server)
- **`server.py`**: A FastMCP server that exposes tools to the AI agent (Roo Code/Cline).
  - It does NOT contain business logic; it wraps functions from `db_manager.py`.
  - Tools: `save_fact`, `retrieve_context`, `write_daily_note`.

### 3. The Configuration
- **`config.py`**: Central hub for constants and Model IDs (e.g., Qwen for logic, Hermes for creative writing).
- **`setup.py`**: A script to dynamically generate the `.roo/mcp.json` configuration with absolute paths, ensuring portability.

## Coding Standards
- **Language**: All code, comments, and documentation must be in English.
- **Style**: Pythonic, snake_case for functions/variables.
- **Dependency Management**: Use `uv` exclusively. (e.g., `uv add package`).
- **Pathing**: Never hardcode absolute paths. Use `pathlib` or dynamic detection via `os.getcwd()`.

## Operational Workflows
- **On Setup**: Run `uv run setup.py` to configure the MCP path for the local machine.
- **On Dev**: When adding a new capability, first implement the logic in `db_manager.py` or a new module, then expose it via `server.py`.