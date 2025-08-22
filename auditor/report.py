from datetime import datetime, timedelta
from typing import List
from .client import KafkaClient
from .models import TopicReport

def generate_report(client: KafkaClient, stale_days: int = 28) -> TopicReport:
    topics = client.list_topics()
    now = datetime.utcnow().isoformat()
    empty, stale, internal = [], [], []
    for t in topics:
        if client.is_internal(t):
            internal.append(t); continue
        min_off, max_off = client.get_offsets(t)
        if max_off - min_off == 0:
            empty.append(t)
        last = client.last_consume_at(t)
        if (datetime.utcnow() - last).days >= stale_days:
            stale.append(t)
    return TopicReport(empty_topics=empty, stale_topics=stale, ignored_internal=internal, generated_at=now)
