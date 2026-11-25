import sys
import streamlit as st
st.session_state["user_data"] = {"stores": [], "role": "admin"}
st.session_state["username"] = "test"
st.session_state["logged_in"] = True

import app
import json

def answer(question, user):
    user_data = app.load_users()[user]
    stores = user_data["stores"]
    intent = app.parse_intent(question)
    
    out = {
        "text": "",
        "rows": [],
        "tokens_in": 0,
        "tokens_out": 0,
        "sql": ""
    }
    
    if intent.get("route", "").startswith("C"):
        out["text"] = "I'm not sure how to answer that."
        return out
        
    try:
        sql, params = app.build_sql(intent, stores)
        out["sql"] = sql
        df = app.execute_query(sql, params)
        if df is not None and not df.empty:
            out["rows"] = df.values.tolist()
            if len(df.columns) == 1 and len(df) == 1:
                out["text"] = str(df.iloc[0, 0])
        out["tokens_in"] = intent.get("tokens", 0)
        out["tokens_out"] = intent.get("tokens", 0)
    except Exception as e:
        out["text"] = str(e)
        
    return out
