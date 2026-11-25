# Final Report

## Architecture Comparison
Based on the evaluated dataset, we compared three architectural approaches:

**A. Deterministic-Only Architecture**
- **Pros:** ~12ms latency, zero API inference cost, zero token consumption.
- **Cons:** Fails on complex, conversational, or ambiguous questions. Intent accuracy drops significantly outside strict keywords.

**B. LLM-Only Architecture**
- **Pros:** High intent accuracy for conversational phrasing.
- **Cons:** ~1200ms latency per query, high token consumption, hits API rate limits at scale, higher API inference costs.

**C. Hybrid Architecture (Implemented)**
- **Pros:** Routes simple queries deterministically (~12ms) and complex queries to the LLM (~1200ms uncached, ~15ms cached). Maximizes accuracy while optimizing cost and speed.
- **Cons:** Increased system complexity. Caching requires careful invalidation and security boundary validation.

## Economics & Projections (API Inference Only)
*Note: API inference cost is distinct from Total Operating Cost (hosting, compute, maintenance).*
- **Baseline Assumption:** 60% queries deterministic ($0), 40% LLM-assisted.
- **1,000 Questions:** ~$0.04
- **10,000 Questions:** ~$0.40
- **100,000 Questions:** ~$4.00

## Caching & Security
- Cached data strictly stores the *abstract intent* (e.g., metric: revenue). 
- User permissions (e.g., store_id filters) are applied dynamically *after* cache retrieval. Permissions are revalidated before executing each database query, ensuring a cached intent never bypasses a user's data scope.

## Production Readiness & Limitations
- **Demo Authentication:** Uses a hardcoded `users.json`. Not production-ready.
- **Model Dependency:** Highly reliant on third-party API uptime and rate limits.
- **Limited Evaluation Coverage:** Tested on 72 questions. Universal accuracy is not guaranteed.
- **Business Logic Gaps:** Independent evaluation showed the current SQL builder requires logic updates for returns and discounts before full production deployment.
