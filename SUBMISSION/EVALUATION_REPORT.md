# Evaluation Report

## Dataset Performance (Independently Validated)
Performance is reported based on an independent reference evaluation script to eliminate circular validation. Expected answers were calculated directly via raw SQL against `retail.db` and compared against the application's outputs.

**Golden Dataset (42 Questions)**
- **Total Questions:** 42
- **Correct Answers:** 32 (76.1%)
- **Incorrect Answers:** 10 (23.9%)

**Holdout Dataset (30 Questions)**
- **Total Questions:** 30
- **Correct Answers:** 21 (70.0%)
- **Incorrect Answers:** 9 (30.0%)

- **Correct Access Denials:** 100% block rate on cross-store unauthorized requests within the test suite.
- **Intent Accuracy:** 95.8% (Hybrid LLM successfully parsed the vast majority of intents).
- **Numerical Accuracy:** 73.6% combined (Discrepancies found).
- **End-to-End Accuracy:** 73.6% combined.

## Discrepancies and Root Causes
1. **Profit Calculation Mismatch:** The application's `build_sql` function calculates profit as `SUM(qty * (unit_price - unit_cost))`. Independent validation revealed this fails to account for `discount_pct` and `is_return` flags in the `sales` table, leading to overstated profit figures.
2. **Aggressive Entity Grouping:** The deterministic route forces a `GROUP BY product_name` if the word "product" appears in the query, causing tabular results to be returned even when a scalar total was expected by the reference metric glossary.

## Route Usage (Combined 72 Queries)
- **Deterministic Route (A):** 45 questions (~62.5%)
- **LLM Route (B):** 27 questions (~37.5%)
- **Clarification Route (C):** 0 triggered by the clean dataset.

## Verification Audit & Limitations
- **Execution Verification:** Evaluation results were generated through actual execution of the pipeline against the database, bypassing self-validation.
- **Security:** Absolute security claims are void; risks are significantly mitigated via parameterized SQL and read-only connections, but not entirely eliminated.

## Economics
- **API Inference Cost:** ~$0.0001 per AI-assisted query (Gemini Flash). 
- **Total Operating Cost:** Must include hosting, compute, database maintenance, and network egress, which are excluded from the pure API inference cost.
- **Tokens:** Avg 150 input / 30 output tokens per LLM query.

## Load Testing
- **Concurrency Levels Tested:** 1, 10, and 50 simulated users. 
- **Untested:** 100+ users (explicitly untested due to local SQLite hardware locks and API rate limit constraints).
- **Test Duration & Throughput:** 60 seconds per tier. Peak throughput ~15 req/sec at 50 users.
- **P95 Latency:** ~2.5s at 50 concurrent users.
- **Errors:** 0 database locks; occasional HTTP 429 rate limits from the LLM provider at peak concurrency.
