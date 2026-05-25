from typing import Literal

from pydantic import BaseModel, Field


class Topic(BaseModel):
    name: str
    partitions: int
    internal: bool = False


class TopicFinding(BaseModel):
    topic: str
    category: Literal["empty", "stale", "internal"]
    reason: str


class TopicReport(BaseModel):
    empty_topics: list[str]
    stale_topics: list[str]  # no consumption since threshold
    ignored_internal: list[str]
    generated_at: str
    findings: list[TopicFinding] = Field(default_factory=list)
