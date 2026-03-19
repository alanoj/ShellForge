from typing import TypedDict, Optional


class LogEvent(TypedDict):
    message: str


class ProgressEvent(TypedDict, total=False):
    advance: int
    total: int


class TaskEvent(TypedDict):
    message: str
