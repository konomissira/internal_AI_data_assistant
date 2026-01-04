from fastapi import FastAPI
from mcp_server.app.tools import catalog

app = FastAPI(
    title="MCP Server (Governed Data Tools)",
    version="0.1.0",
    description="HTTP-based MCP-style tool server for governed access to analytics data.",
)


@app.get("/health")
def health():
    return {"status": "ok"}


# MCP-style tools (v1)
@app.get("/tools/catalog/list-metrics")
def catalog_list_metrics():
    return {"tool": "catalog.list_metrics", "data": catalog.list_metrics()}
