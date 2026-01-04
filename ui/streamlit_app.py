import os
import pandas as pd
import streamlit as st

from ai_service.app.orchestrator import answer_question


st.set_page_config(page_title="Internal AI Data Assistant", layout="wide")

st.title("Internal AI Data Assistant Platform (MCP-Governed)")
st.caption("Ask a business question → governed SQL → safe execution → observable results")

# Config
default_mcp_url = os.getenv("MCP_BASE_URL", "http://localhost:8000")
mcp_base_url = st.sidebar.text_input("MCP Server URL", value=default_mcp_url)

st.sidebar.markdown("### Example questions")
examples = [
    "Total sales by region",
    "Average order value by region",
    "Total quantity by product",
    "Total orders by category",
]
for ex in examples:
    if st.sidebar.button(ex):
        st.session_state["question"] = ex

question = st.text_input("Your question", value=st.session_state.get("question", ""))

col1, col2 = st.columns([1, 1])
run = col1.button("Run", type="primary")
clear = col2.button("Clear")

if clear:
    st.session_state["question"] = ""
    st.rerun()

if run:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating governed SQL and executing..."):
            out = answer_question(mcp_base_url=mcp_base_url, question=question)

        st.subheader("Plan")
        st.write({
            "ok": out.get("ok"),
            "metric": out.get("metric"),
            "dimensions": out.get("dimensions"),
        })

        st.subheader("SQL")
        st.code(out.get("executed_sql") or out.get("sql") or "", language="sql")

        if not out.get("ok"):
            st.error("Request blocked or failed.")
            st.write(out)
        else:
            result = out["result"]
            rows = result.get("rows", [])
            st.subheader("Results")

            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Query returned no rows.")
