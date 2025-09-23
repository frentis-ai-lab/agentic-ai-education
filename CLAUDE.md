# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an educational repository for Korean-speaking students learning Agentic AI concepts. It contains 10 step-by-step lessons demonstrating different AI frameworks and patterns. Each lesson is a self-contained Python project using `uv` package manager.

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
- `08_a2a_basics/`: `uv run python basic_chat.py`

## Architecture

### Lesson Structure
- **01**: LangChain ReAct agents with basic tools
- **02-03**: FastMCP (Model Control Protocol) tool creation and packaging
- **04**: LangChain ReAct agents with MCP tool integration
- **05-06**: mem0 memory management for personalized AI
- **07**: CrewAI collaborative workflows
- **08-10**: AutoGen agent-to-agent communication patterns

### Dependencies
Each lesson uses minimal, focused dependencies:
- FastMCP lessons: `fastmcp>=2.12,<3.0`
- LangChain lessons: `langchain-openai`, `langchain-community`
- CrewAI lessons: `crewai>=0.193.0`
- mem0 lessons: `mem0ai>=0.1.20`
- AutoGen lessons: `pyautogen>=0.4.0`

### API Keys Required
- `OPENAI_API_KEY`: Used in lessons 01, 04, 05, 06, 08
- `MEM0_API_KEY`: Used in lessons 05, 06
- `OPENAI_MODEL`: Optional, defaults to `gpt-4o-mini`

## Important Notes

### Korean Learning Context
This repository is designed for Korean-speaking students learning Agentic AI. Keep examples simple and educational-focused rather than production-ready. The target audience values clear, minimal examples over complex implementations.

### uv Package Manager
All lessons use `uv` instead of pip/poetry. Each lesson has its own `pyproject.toml` with `package = false` setting, making them runnable projects rather than installable packages.

### Docker Disabled
AutoGen lessons explicitly set `use_docker=False` to avoid Docker dependencies in educational environments.