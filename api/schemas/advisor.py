from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from api.schemas.validators import (
    MAX_QUERY_CHARS,
    MAX_RESULTS_ITEMS,
    validate_repo_payload,
    validate_results_list,
)


class ExplainRepoRequest(BaseModel):
    repo: Dict[str, Any]
    profile: Optional[Dict[str, Any]] = None
    query: Optional[str] = Field(default=None, max_length=MAX_QUERY_CHARS)
    score_breakdown: Optional[Dict[str, float]] = None
    include_roadmap: bool = True

    @field_validator("repo")
    @classmethod
    def _check_repo(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        return validate_repo_payload(value)


class RoadmapRequest(BaseModel):
    repo: Dict[str, Any]
    profile: Optional[Dict[str, Any]] = None

    @field_validator("repo")
    @classmethod
    def _check_repo(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        return validate_repo_payload(value)


class CompareReposRequest(BaseModel):
    repo_a: Dict[str, Any]
    repo_b: Dict[str, Any]
    profile: Optional[Dict[str, Any]] = None
    query: Optional[str] = Field(default=None, max_length=MAX_QUERY_CHARS)

    @field_validator("repo_a", "repo_b")
    @classmethod
    def _check_repo(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        return validate_repo_payload(value)


class AdvisorSummaryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=MAX_QUERY_CHARS)
    profile: Dict[str, Any] = Field(default_factory=dict)
    results: List[Dict[str, Any]] = Field(..., max_length=MAX_RESULTS_ITEMS)
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator("results")
    @classmethod
    def _check_results(cls, value: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return validate_results_list(value)
