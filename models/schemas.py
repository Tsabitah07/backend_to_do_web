"""
models/schemas.py
─────────────────
Pydantic schemas untuk validasi request/response.
"""

from pydantic import BaseModel, field_validator
from typing import Optional, Literal

VALID_PRIORITIES = {"low", "medium", "high"}
VALID_POSITIONS  = {"start", "end"}


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: Literal["low", "medium", "high"] = "medium"
    status: Literal["todo", "in_progress", "done"] = "todo"
    position: str = "end"   # "start" | "end" | <task_id>

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title tidak boleh kosong")
        return v.strip()


class TaskUpdate(BaseModel):
    title:       Optional[str]  = None
    description: Optional[str]  = None
    priority:    Optional[Literal["low", "medium", "high"]] = None
    status:      Optional[Literal["todo", "in_progress", "done"]] = None
    completed:   Optional[bool] = None


class TaskResponse(BaseModel):
    task_id:     str
    title:       str
    description: str
    priority:    str
    status:      str
    completed:   bool
    created_at:  str


class TaskListResponse(BaseModel):
    tasks:     list[TaskResponse]
    total:     int
    structure: str = "Singly Linked List"


class OperationResponse(BaseModel):
    task:       TaskResponse
    operation:  str
    list_size:  int


class VizNode(BaseModel):
    index:    int
    task_id:  str
    title:    str
    has_next: bool
    next_id:  Optional[str]


class VizResponse(BaseModel):
    head:  Optional[str]
    nodes: list[VizNode]
    size:  int
