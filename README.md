# Agentic AI Course Management System

An educational project exploring agent-based course management through tools, reusable skills, memory, connectors, and runtime concepts.

## Project Overview

The project is organized into individual labs, each exploring a different component of an agentic system.

## Implemented Labs

### Lab 1 — Basic Agent

* Rule-based chatbot
* Tool-using agent

### Lab 2 — Tools and API

* Course management tools
* Safe calculator
* File operations
* HTTP API integration

### Lab 3 — Reusable Skills

* Course management skill
* Calculator skill
* File management skill

### Lab 4 — Memory

* Short-term session memory
* Persistent long-term memory
* Keyword-based memory retrieval

### Lab 5 — Connector Architecture

* File connector
* SQLite course database
* HTTP API connector
* Connector registry
* Unit tests

### Lab 6 — Runtime Integration

Planned: runtime execution, logging, and audit trail, with the specific OpenClaw integration approach to be determined.

## Technology Stack

* Python
* SQLite
* FastAPI / Uvicorn
* JSON
* Python unittest
* HTTP APIs

## Project Structure

```text
Agentic_AI/
├── lab1/
├── lab2/
├── lab3/
├── lab4/
├── lab5/
└── README.md
```

## Running the Tests

From the project root:

```bash
python -m unittest lab3.test_skills -v
python -m unittest lab4.test_memory -v
python -m unittest lab5.test_connectors -v
```

## Running Lab 5

Start the Lab 2 API server in one terminal:

```bash
python -m uvicorn lab2.api_server:app --reload --port 8000
```

In another terminal, start the Lab 5 agent:

```bash
python -m lab5.agent
```

Type `help` to see the supported commands.

## Project Status

Labs 1–5 have been implemented and tested. Lab 6 runtime integration is planned.

## Disclaimer

This is an educational project. Features described as planned are not represented as completed.
