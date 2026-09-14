from typing import Literal

from pydantic import BaseModel, Field


class ReviewFinding(BaseModel):
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    category: str
    file: str | None = None
    line: str | None = None
    description: str
    recommendation: str


class ReviewResult(BaseModel):
    issues: list[ReviewFinding] = Field(default_factory=list)