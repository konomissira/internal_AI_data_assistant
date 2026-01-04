# Internal AI Data Assistant Platform (MCP-Governed)

A **production-minded internal AI data platform** that enables business users to ask questions in natural language and receive **trusted, governed answers** via AI-generated SQL.

The platform uses **MCP (Model Context Protocol)** as the interface layer and enforces:

-   governance
-   safety
-   observability
-   evaluation

This is **not a GenAI demo**.  
It is a realistic internal data platform designed for enterprise environments.

---

## Why this project

GenAI demos are easy to build. **Production systems are not**.

Most GenAI initiatives fail in real organisations not because of the model, but because of weak data foundations:

-   unclear semantic definitions of metrics
-   uncontrolled access to raw tables
-   unsafe or incorrect SQL generation
-   no observability or evaluation
-   no way to measure trust or regressions

This project focuses on the **data engineering foundations** required to make AI assistants **reliable, auditable, and safe to deploy**.

---

## What this platform demonstrates

-   **MCP-governed tool interfaces** (catalog, SQL validation, execution)
-   **Semantic layer–driven analytics** (metrics, dimensions, joins)
-   **SQL safety and policy enforcement**
-   **Full telemetry and observability**
-   **Golden-questions evaluation suite**
-   **End-to-end orchestration from question → answer**
-   **Senior engineering discipline** (clear boundaries, testing, evaluation)

---

## Core capabilities

### MCP Server

-   Dataset and metric discovery
-   Semantic model access
-   SQL validation (SELECT-only, allowlisted tables, LIMIT enforcement)
-   Safe query execution
-   Telemetry logging

### AI Orchestration Layer

-   Question intent parsing (metric + dimensions)
-   Governed SQL generation
-   Validation → execution workflow
-   Replaceable planner (rule-based now, LLM-ready later)

### Evaluation Layer

-   Golden questions test suite
-   Pass/fail reporting
-   Regression detection for intent parsing and safety

### UI (Streamlit)

-   Natural language question input
-   Generated SQL visibility
-   Result tables
-   Business-friendly demo experience

---

## High-level architecture

```
[ Business User ]
        |
        v
[ Streamlit UI ]
        |
        v
[ AI Orchestrator ]
        |
        v
[ MCP Server ]
  |   |    |
  |   |    +--> SQL validation
  |   |
  |   +--> Semantic catalog
  |
  +--> Safe query execution
        |
        v
[ Analytics Database ]
        |
        v
[ Telemetry + Evaluation ]
```

**Key principle:**  
This is a **data platform first**.  
AI is an interface — not the system.

---

## Repository structure

```
.
├── docker/                 # Container orchestration (Postgres, services)
├── db/
│   └── init/               # Schema, seed data, semantic layer
├── mcp_server/             # MCP server (tools, governance, telemetry)
├── ai_service/             # AI orchestration logic
├── ui/                     # Streamlit demo UI
├── evaluation/             # Golden questions & evaluation runner
│   └── reports/
└── docs/                   # Architecture diagrams and demo scripts
```

---

## Quick start (local, non-docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start services:

```bash
# Terminal 1
docker compose up -d postgres

# Terminal 2
uvicorn mcp_server.app.main:app --reload --port 8000

# Terminal 3
python -m streamlit run ui/streamlit_app.py
```

---

## Evaluation (Golden Questions)

Run evaluation:

```bash
python -m evaluation.run_eval
```

Outputs:

-   Console summary
-   Detailed report: `evaluation/reports/latest.json`

---

## Design principles

-   **Governance over freedom**
-   **Observability by default**
-   **Evaluation as a first-class concern**
-   **Clear separation of responsibilities**
-   **Production realism over novelty**

---

## Roadmap

-   [x] Governed MCP server
-   [x] Semantic analytics layer
-   [x] SQL validation & safety
-   [x] Telemetry & logging
-   [x] Streamlit demo UI
-   [x] Golden questions evaluation suite
-   [ ] Full dockerised one-command demo

---

## License

MIT License
