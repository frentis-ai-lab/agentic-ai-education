# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an educational repository for Korean-speaking students learning Agentic AI concepts. It contains 11 step-by-step lessons demonstrating different AI frameworks and patterns. Each lesson is a self-contained Python project using `uv` package manager.

## Key Commands

### Environment Setup
```bash
# Copy and configure environment variables
cp .env.example .env
source .env
```

### Running Lessons
Each lesson directory has its own dependencies. Navigate to any lesson folder and:
```bash
uv sync                    # Install dependencies
uv run python <script.py>  # Run the main script
```

### Common Scripts by Lesson
- `01_langchain_react/`: `uv run python react_agent.py`
- `02_fastmcp_tool/`: `uv run python server.py` and `uv run python client.py`
- `03_fastmcp_email/`: `uv run python server.py` and `uv run python client.py`
- `09_crewai_mcp/`: `uv run python newsletter_crew.py --email recipient@example.com`
- `10_a2a_airbnb/`: Navigate to each agent subfolder and `uv run .`

## Architecture

### Lesson Structure
- **01**: LangChain ReAct agents with basic tools
- **02-04**: FastMCP (Model Control Protocol) tool creation, email integration, and packaging
- **05**: LangChain ReAct agents with MCP tool integration
- **06-07**: mem0 memory management for personalized AI
- **08-09**: CrewAI collaborative workflows and MCP integration
- **10**: Google A2A SDK multi-agent systems
- **11**: Future technology exploration and project planning

### Dependencies
Each lesson uses minimal, focused dependencies:
- FastMCP lessons: `fastmcp>=2.12,<3.0`
- LangChain lessons: `langchain-openai`, `langchain-community`
- CrewAI lessons: `crewai>=0.193.0`
- mem0 lessons: `mem0ai>=0.1.20`
- Google A2A lessons: `a2a-sdk` (requires Python 3.13)

### API Keys Required
- `OPENAI_API_KEY`: Used in lessons 01, 03, 05, 06, 07, 08, 09
- `MEM0_API_KEY`: Used in lessons 06, 07
- `GOOGLE_API_KEY`: Used in lesson 10 (A2A SDK)
- `GMAIL_USER` & `GMAIL_APP_PASSWORD`: Used in lessons 03, 09 (email functionality)
- `OPENAI_MODEL`: Optional, defaults to `gpt-4o-mini`

## Important Notes

### Korean Learning Context
This repository is designed for Korean-speaking students learning Agentic AI. Keep examples simple and educational-focused rather than production-ready. The target audience values clear, minimal examples over complex implementations.

### uv Package Manager
All lessons use `uv` instead of pip/poetry. Each lesson has its own `pyproject.toml` with `package = false` setting, making them runnable projects rather than installable packages.

### Python Version Requirements
- Most lessons work with Python 3.11+
- Google A2A SDK (lesson 10) specifically requires Python 3.13
- Use pyenv or conda to manage multiple Python versions if needed