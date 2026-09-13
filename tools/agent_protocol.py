"""Untrusted worker proposals. Validation never authorizes execution."""

from pathlib import PurePosixPath
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FileProposal(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    path: str
    content: str = Field(max_length=30000)

    @field_validator("path")
    @classmethod
    def relative_path(cls, value: str) -> str:
        p = PurePosixPath(value)
        if not value or p.is_absolute() or ".." in p.parts or "\\" in value or ":" in value:
            raise ValueError("Only repository-relative POSIX paths are accepted")
        return value


class AgentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    task_id: str
    status: Literal["completed", "blocked", "needs_review"]
    summary: str = Field(max_length=800)
    files_to_create: list[FileProposal] = Field(max_length=4)
    files_to_modify: list[FileProposal] = Field(max_length=4)
    patch: str
    tests_proposed: list[str] = Field(max_length=8)
    assumptions: list[str] = Field(max_length=6)
    risks: list[str] = Field(max_length=6)
    questions: list[str] = Field(max_length=3)

    def check_scope(self, task_id: str, allowed: set[str]) -> None:
        if self.task_id != task_id:
            raise ValueError("Task identity mismatch")
        paths = [p.path for p in self.files_to_create + self.files_to_modify]
        if len(paths) != len(set(paths)) or not set(paths) <= allowed:
            raise ValueError("Duplicate or out-of-scope file proposal")
        if self.patch:
            raise ValueError("Use scoped file proposals; free-form patches are not accepted")
