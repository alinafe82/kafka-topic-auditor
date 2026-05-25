from pydantic import BaseModel


class Topic(BaseModel):
    name: str
    partitions: int
    internal: bool = False

class TopicReport(BaseModel):
    empty_topics: list[str]
    stale_topics: list[str]  # no consumption since threshold
    ignored_internal: list[str]
    generated_at: str
