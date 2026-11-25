# Presentation Notes

## 30-Second Opening
"Store managers need instant, trusted numbers to make daily decisions, but traditional dashboards are rigid and raw AI is too risky. RetailIQ solves this through a Hybrid Intelligence architecture. By parsing natural language into safe, parameterized intents, we deliver strong intent accuracy, returning deterministic answers in ~12 milliseconds while significantly mitigating unauthorized data access."

## 5-Minute Live Demonstration
1. **Login:** Log in as `ana` (single-store access).
2. **Deterministic Route:** Ask "total revenue". Show the ~12ms response and the Route A indicator.
3. **AI-Assisted Route:** Ask "compare profit between in-store and online". Show the ~1.2s response via Route B.
4. **Security Block:** Ask "show me all stores revenue". Show the backend blocking the request and enforcing only Ana's assigned store.
5. **HQ Login:** Log in as `hq`. Run the same query to demonstrate cross-store access functioning for authorized users.

## The 8 Assignment Stages
1. **PRD:** Defined the core problem and user roles.
2. **Golden Dataset:** 42 golden questions + 30 holdout questions.
3. **Architecture:** Hybrid routing (Deterministic + LLM).
4. **Decision Log:** Justified Gemini Flash via OpenRouter for cost/speed balance.
5. **Build Plan:** Iterative slice-based development.
6. **Application:** Streamlit UI with `?mode=ro` SQLite read-only backend.
7. **Evaluation:** Independent baseline calculation to prevent circular validation.
8. **Verdict:** Controlled Pilot recommendation.

## 20 Difficult Q&A
1. **Q:** Is this 100% accurate? **A:** No. Independent evaluation on the holdout set returned a 70% numerical accuracy rate due to missing business logic around product returns and discounts.
2. **Q:** Are security risks completely eliminated? **A:** No system is impenetrable. Absolute risks are never fully eliminated, but they are significantly mitigated via parameterized SQL and read-only DB connections.
3. **Q:** Did you independently calculate the expected answers? **A:** Yes. In the final phase, we broke circular validation by calculating expected answers outside the app's query builder. This is how we identified the discount/return discrepancies.
4. **Q:** What is the actual latency? **A:** ~12ms deterministic, ~15ms cached AI, ~1.2s uncached AI.
5. **Q:** Is the API cost the only cost? **A:** No, the API inference cost is distinct from Total Operating Cost (hosting, database, network egress).
*(Continue with remaining questions on scale, caching, and model failure fallbacks)*

## Limitations & Future Improvements
- Uses mock authentication (`users.json`).
- Untested beyond 50 concurrent users.
- Highly dependent on third-party model availability.
- SQL Builder must be updated to factor in `is_return` and `discount_pct`.
