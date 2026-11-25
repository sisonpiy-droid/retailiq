with open('C:/Users/sison/ai-builds/BuildDay/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Add requests
text = text.replace('import time', 'import time\nimport requests')

replacement = """OPENROUTER_API_KEY = "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"

def deterministic_route(q):
    intent = {"metric": "revenue", "entity": "all", "is_safe": True}
    if "profit" in q: intent["metric"] = "profit"
    elif "quantity" in q or "qty" in q or "sold" in q: intent["metric"] = "qty"
    if "product" in q or "item" in q: intent["entity"] = "product"
    unsafe_words = ["drop", "delete", "update", "insert", "ignore", "bypass", "admin"]
    if any(w in q for w in unsafe_words): intent["is_safe"] = False
    return intent

def llm_route(q):
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Parse the intent of the following question. Return ONLY a JSON object with 'metric' (e.g. revenue, profit, qty, discount, traffic), 'entity' (e.g. all, product, category, city), and 'is_safe' (boolean). Do not return any raw SQL or other text. Question: {q}"
    data = {"model": "google/gemini-2.5-flash", "messages": [{"role": "user", "content": prompt}]}
    start = time.time()
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"].strip()
        content = content.replace("```json", "").replace("```", "").strip()
        intent = json.loads(content)
        intent["route"] = "B (LLM)"
        intent["latency"] = time.time() - start
        intent["tokens"] = response_json.get("usage", {}).get("total_tokens", 0)
        return intent
    except Exception as e:
        return {"metric": "unknown", "entity": "unknown", "is_safe": True, "route": "C (Clarification)", "error": str(e)}

@st.cache_data(ttl=3600)
def parse_intent(question):
    q = question.lower()
    simple_keywords = ["revenue", "profit", "qty", "quantity", "sold", "product", "item"]
    complex_keywords = ["average", "trend", "discount", "margin", "traffic", "category", "city", "region"]
    if any(k in q for k in complex_keywords): return llm_route(question)
    elif any(k in q for k in simple_keywords):
        intent = deterministic_route(q)
        intent["route"] = "A (Deterministic)"
        return intent
    else: return {"metric": "unknown", "entity": "unknown", "is_safe": True, "route": "C (Clarification)"}

def build_sql"""

text = re.sub(r'def parse_intent\(question\):.*?def build_sql', replacement, text, flags=re.DOTALL)

with open('C:/Users/sison/ai-builds/BuildDay/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
