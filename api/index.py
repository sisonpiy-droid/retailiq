import json
import sqlite3
import pandas as pd
import time
import requests
import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Configure Enterprise-Grade Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RetailIQ-Backend")

app = FastAPI(
    title="RetailIQ Analytics Engine",
    description="Next-generation hybrid AI analytics engine for enterprise retail.",
    version="2.0.0"
)

DB_PATH = "retail.db"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "sk-or-...1be7")

def get_db_connection():
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, check_same_thread=False)

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def deterministic_route(q: str):
    intent = {"metric": "revenue", "entity": "all", "is_safe": True}
    if "profit" in q: intent["metric"] = "profit"
    elif "quantity" in q or "qty" in q or "sold" in q: intent["metric"] = "qty"
    if "product" in q or "item" in q: intent["entity"] = "product"
    unsafe_words = ["drop", "delete", "update", "insert", "ignore", "bypass", "admin"]
    if any(w in q for w in unsafe_words): intent["is_safe"] = False
    return intent

def llm_route(q: str):
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Parse the intent of the following question. Return ONLY a JSON object with 'metric' (e.g. revenue, profit, qty, discount, traffic), 'entity' (e.g. all, product, category, city), and 'is_safe' (boolean). Do not return any raw SQL or other text. Question: {q}"
    data = {"model": "google/gemini-2.5-flash", "messages": [{"role": "user", "content": prompt}]}
    start = time.time()
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=10)
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"].strip()
        content = content.replace("```json", "").replace("```", "").strip()
        intent = json.loads(content)
        intent["route"] = "B (LLM)"
        intent["latency"] = time.time() - start
        return intent
    except Exception as e:
        return None

def parse_intent(question: str):
    """Hybrid routing logic determining whether to use regex deterministic paths or LLM."""
    q = question.lower()
    simple_keywords = ["revenue", "profit", "qty", "quantity", "sold", "product", "item"]
    complex_keywords = ["average", "trend", "discount", "margin", "traffic", "category", "city", "region"]
    
    intent = None
    if any(k in q for k in complex_keywords): 
        intent = llm_route(question)
    elif any(k in q for k in simple_keywords):
        intent = deterministic_route(q)
        intent["route"] = "A (Deterministic)"
        
    if intent is None or not intent.get("is_safe", True) or intent.get("metric") not in ["revenue", "profit", "qty"]:
        # Fallback mechanism
        fallback = {"metric": "revenue", "entity": "all", "is_safe": True, "route": "Fallback", "fallback": True}
        return fallback
        
    return intent

def build_sql(intent, user_stores, q=""):
    """Builds parameterized SQL enforcing Row-Level Security via store_id constraints."""
    store_placeholder = ', '.join(['?'] * len(user_stores))
    params = list(user_stores)
    
    queries = {
        "revenue": f"SELECT SUM(qty * unit_price * (1.0 - COALESCE(discount_pct, 0.0))) as val FROM sales WHERE is_return = 0 AND store_id IN ({store_placeholder})",
        "profit": f"SELECT SUM(s.qty * (s.unit_price * (1.0 - COALESCE(s.discount_pct, 0.0)) - p.unit_cost)) as val FROM sales s JOIN products p ON s.product_id = p.product_id WHERE s.is_return = 0 AND s.store_id IN ({store_placeholder})",
        "qty": f"SELECT SUM(qty) as val FROM sales WHERE is_return = 0 AND store_id IN ({store_placeholder})"
    }
    
    if intent.get("entity") == "product" and "by product" in q.lower():
        queries["revenue"] = f"SELECT p.product_name, SUM(s.qty * s.unit_price * (1.0 - COALESCE(s.discount_pct, 0.0))) as val FROM sales s JOIN products p ON s.product_id = p.product_id WHERE s.is_return = 0 AND s.store_id IN ({store_placeholder}) GROUP BY p.product_name ORDER BY val DESC LIMIT 5"
    
    return queries.get(intent.get("metric", "revenue"), queries["revenue"]), params

def execute_query(sql, params):
    try:
        conn = get_db_connection()
        df = pd.read_sql(sql, conn, params=params)
        conn.close()
        return df
    except Exception:
        return None

class LoginRequest(BaseModel):
    username: str

@app.post("/api/login")
def login(req: LoginRequest):
    users = load_users()
    if req.username in users:
        return {"success": True, "user": users[req.username], "username": req.username}
    return JSONResponse(status_code=401, content={"error": "User not found"})

class MetricsRequest(BaseModel):
    stores: List[str]

@app.post("/api/metrics")
def metrics(req: MetricsRequest):
    sql_rev, params_rev = build_sql({"metric": "revenue", "entity": "all", "is_safe": True}, req.stores)
    df_rev = execute_query(sql_rev, params_rev)
    rev = float(df_rev.iloc[0]['val']) if (df_rev is not None and not df_rev.empty and not pd.isna(df_rev.iloc[0]['val'])) else 0
    
    sql_prof, params_prof = build_sql({"metric": "profit", "entity": "all", "is_safe": True}, req.stores)
    df_prof = execute_query(sql_prof, params_prof)
    prof = float(df_prof.iloc[0]['val']) if (df_prof is not None and not df_prof.empty and not pd.isna(df_prof.iloc[0]['val'])) else 0
    
    return {"revenue": rev, "profit": prof}

class ChatRequest(BaseModel):
    question: str
    stores: List[str]

@app.post("/api/chat")
def chat(req: ChatRequest):
    start = time.time()
    intent = parse_intent(req.question)
    
    sql, params = build_sql(intent, req.stores, req.question)
    df = execute_query(sql, params)
    elapsed = time.time() - start
    
    if df is not None and not df.empty:
        # Convert DataFrame to records
        if len(df.columns) == 1 and len(df) == 1:
            data = {"type": "scalar", "value": float(df.iloc[0, 0]) if not pd.isna(df.iloc[0, 0]) else 0}
        else:
            data = {"type": "table", "data": df.to_dict(orient="records"), "columns": list(df.columns)}
    else:
        data = {"type": "empty"}
        
    return {
        "intent": intent,
        "sql": sql,
        "time": elapsed,
        "result": data
    }
