# kafka-topic-auditor
> Audit Kafka topics for emptiness and recent consumption to flag candidates for cleanup

This project demonstrates production-aware logic for topic hygiene:
- Excludes internal topics
- Flags topics with **no consumption in N days**
- Detects **empty topics** using offsets
- Produces a Markdown or JSON report

The code uses an interface layer you can wire to your Kafka admin client; a local mock is provided for demos/tests.
