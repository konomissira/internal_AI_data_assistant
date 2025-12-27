# Internal AI Data Assistant Platform (MCP-Governed)

A **governed internal data platform** that enables business users to ask questions in natural language and receive trusted answers via **AI-generated SQL**, using **MCP (Model Context Protocol) as the interface layer**.
The system enforces **guardrails**, and provides **logging, evaluation, and observability** to support production-style deployment.

---

## Why this project

GenAI demos are easy to build. Production systems are not.

Most GenAI projects fail in real environments not because of the model, but because of weak data foundations, including:

-   unclear semantic definitions of metrics
-   uncontrolled access to raw tables
-   unsafe or incorrect SQL generation
-   lack of observability and evaluation

This project focuses on the **data engineering foundations** required to make AI assistants **reliable, auditable, and production-ready**.

---

## Core capabilities (MVP)

-   **MCP Server** exposing governed tools for:
    -   dataset and metric discovery (catalog)
    -   semantic model access (joins, dimensions, constraints)
    -   SQL generation and validation
    -   safe query execution
    -   telemetry and logging
-   **Semantic layer & governance**
    -   approved metrics and dimensions
    -   controlled joins and constraints
    -   SQL policy enforcement
-   **Evaluation layer**
    -   golden questions test suite
    -   automated checks for validity and performance
-   **Minimal UI**
    -   CLI or Streamlit interface for querying data
    -   visibility into generated SQL, results, and evaluation status

---

## High-level architecture

```
[ Business User ]
        |
        v
[ UI / Client ]
        |
        v
[ AI Query Service ]
        |
        v
[ MCP Server (tools + governance) ]
        |
        v
[ Analytics Database ]
        |
        v
[ Logs + Evaluation ]
```

**Key principle:**  
This is a **data platform first**.  
AI is an interface, not the system.

---

## Repository structure

```
.
├── docker/                 # Local infrastructure (PostgreSQL, etc.)
├── db/
│   └── init/               # Schema, seed data, semantic layer SQL
├── mcp_server/             # MCP server (tools, governance, telemetry)
│   ├── app/
│   │   ├── tools/
│   │   ├── governance/
│   │   └── db/
│   └── tests/
├── ai_service/             # AI orchestration service (calls MCP tools)
│   ├── app/
│   │   └── prompts/
│   └── tests/
├── ui/                     # Minimal interface Streamlit
├── evaluation/             # Golden questions + evaluation scripts
│   └── reports/
└── docs/                   # Architecture diagrams and demo scripts
```

---

## Local setup (initial)

### 1. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Roadmap (tracked via milestones)

-   [x] Repository bootstrap and documentation
-   [ ] Analytics database schema and seed data
-   [ ] MCP server skeleton and core tools
-   [ ] Semantic layer and SQL governance rules
-   [ ] Logging and evaluation framework
-   [ ] Minimal UI and demo workflow

---

## Design goals

-   **Governance over freedom**: AI queries operate only within approved boundaries
-   **Observability by default**: every query is logged and evaluated
-   **Production realism**: prioritise reliability over novelty
-   **Senior-level discipline**: clean architecture, clear contracts, versioned changes

---

## License

MIT License
