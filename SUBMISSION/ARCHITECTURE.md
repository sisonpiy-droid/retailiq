# Architecture Document (Updated)
- **Frontend**: Streamlit.
- **Backend/DB**: SQLite in read-only mode (`retail.db`).
- **Intelligence Layer**:
  - Route A: Regex/Keyword based deterministic matching.
  - Route B: OpenRouter API (`google/gemini-2.5-flash`) intent parser.
  - Route C: Clarification fallback.
- **Security**: The LLM *never* generates SQL. It outputs a standardized JSON intent payload, which the Python backend maps to safe, parameterized SQL templates.
