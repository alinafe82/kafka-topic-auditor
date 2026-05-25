from datetime import UTC, datetime, timedelta

# Mockable interface. Replace with real Kafka admin and consumer-group wiring.
INTERNAL_PREFIXES = ("__consumer_offsets", "_schema", "_confluent", "__transaction_state")

class KafkaClient:
    def list_topics(self) -> list[str]:
        return ["orders", "payments", "dead-letter", "__consumer_offsets"]

    def is_internal(self, topic: str) -> bool:
        return topic.startswith(INTERNAL_PREFIXES)

    def get_offsets(self, topic: str) -> tuple[int, int]:
        # (min, max) per topic across partitions simplified
        return (0, 0) if topic == "dead-letter" else (0, 100)

    def last_consume_at(self, topic: str) -> datetime:
        if topic == "payments":
            return datetime.now(UTC) - timedelta(days=40)
        return datetime.now(UTC) - timedelta(days=1)
