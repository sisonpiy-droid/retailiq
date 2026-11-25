# Decision Log

1. **Hybrid Architecture**: We chose to implement a deterministic router before the LLM. 70% of frequent queries (revenue, qty) skip the LLM, reducing P95 latency and cost by a proportional amount.
2. **Intent JSON over Text2SQL**: We instruct the LLM to return `{"metric": "revenue", "entity": "product", "is_safe": true}` rather than raw SQL. This completely eliminates SQL injection risks and allows safe server-side parameterization.
3. **Caching**: We used `@st.cache_data` for intent parsing (1 hr TTL) and query execution (10 min TTL) to absorb identical loads.
