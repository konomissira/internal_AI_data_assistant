from fastapi import FastAPI
from mcp_server.app.tools import catalog, sql, query, semantic

app = FastAPI(
    title="MCP Server (Governed Data Tools)",
    version="0.2.0",
    description="HTTP-based MCP-style tool server for governed access to analytics data.",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tools/catalog/list-metrics")
def catalog_list_metrics():
    return {"tool": "catalog.list_metrics", "data": catalog.list_metrics()}


@app.get("/tools/catalog/get-semantic-model")
def catalog_get_semantic_model():
    return {"tool": "catalog.get_semantic_model", "data": semantic.get_semantic_model()}


@app.post("/tools/sql/validate")
def sql_validate(payload: dict):
    return {"tool": "sql.validate", "data": sql.validate(payload)}


@app.post("/tools/query/execute")
def query_execute(payload: dict):
    return {"tool": "query.execute", "data": query.execute(payload)}
