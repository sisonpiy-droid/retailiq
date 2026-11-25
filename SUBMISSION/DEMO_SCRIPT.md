# Demo Script

1. **Login**: Log in as `hq` to show the full dashboard, then `ana` to demonstrate store-level isolation.
2. **Dashboard Overview**: Point out the instantaneous load time due to deterministic queries.
3. **Ask RetailIQ (Simple)**: Type "What is our total revenue?". Show that Route A (Deterministic) was taken in <10ms.
4. **Ask RetailIQ (Complex)**: Type "Which products had the highest margins?". Show Route B (LLM) processing the intent into JSON, then querying safely.
5. **Security**: Type "Drop table sales". Show the system rejecting it ("Malicious intent blocked").
6. **Evaluation**: Go to Evaluation tab, click Run to show 42/42 defensive tests passing.
