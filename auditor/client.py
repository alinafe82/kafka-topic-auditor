from typing import Dict, List, Tuple
from datetime import datetime, timedelta

# Mockable interface — replace with real Kafka client wiring.
INTERNAL_PREFIXES = ("__consumer_offsets", "_schema", "_confluent", "__transaction_state")

class KafkaClient:
    def list_topics(self) -> List[str]:
        return ["orders", "payments", "dead-letter", "__consumer_offsets"]
    def is_internal(self, topic: str) -> bool:
        return topic.startswith(INTERNAL_PREFIXES)
    def get_offsets(self, topic: str) -> Tuple[int, int]:
        # (min, max) per topic across partitions simplified
        return (0, 0) if topic == "dead-letter" else (0, 100)
    def last_consume_at(self, topic: str) -> datetime:
        if topic == "payments":
            return datetime.utcnow() - timedelta(days=40)
        return datetime.utcnow() - timedelta(days=1)
