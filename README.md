# Orthanc 👁️

> A local, privacy-focused Digital Twin and autonomous agent system.

Orthanc is a personal AI infrastructure designed to run locally (using LM Studio and local Python scripts). It acts as a bridge between Large Language Models and the local operating system, allowing for persistent memory, context retrieval, and automated actions.

## 🏗 Architecture

The system follows a modular "Brain-Hands-Eyes" architecture:

- **Brain**: Hybrid memory system using **SQLite** (relational data) and **ChromaDB** (vector/semantic memory).
- **Hands**: An **MCP (Model Context Protocol)** server that exposes local tools (Database access, File I/O, Browser Automation) to the AI Agent.
- **Engine**: Powered by local LLMs via **LM Studio** (Qwen 2.5 Coder, Hermes 4, etc.).

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (Fast Python package installer)
- VS Code with [Roo Code](https://github.com/RooVetGit/Roo-Code) extension
- LM Studio (running a local server on port 1234)

### Installation

1. **Clone the repository**
```bash
git clone [https://github.com/yourusername/orthanc.git](https://github.com/yourusername/orthanc.git)
```
```bash
cd orthanc
```

Initialize Environment
```bash
uv sync
```

Configure MCP Run the setup script to inject the absolute path into Roo Code's settings:

```bash
uv run setup.py
```
Activate in Roo Code

Open the "MCP Servers" panel in Roo Code.

Click "Refresh".

Ensure clone-brain is green.