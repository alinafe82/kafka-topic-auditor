from pydantic import BaseModel
from typing import Dict, List, Optional

class Topic(BaseModel):
    name: str
    partitions: int
    internal: bool = False

class TopicReport(BaseModel):
    empty_topics: List[str]
    stale_topics: List[str]  # no consumption since threshold
    ignored_internal: List[str]
    generated_at: str
