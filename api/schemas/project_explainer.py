from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator

from api.schemas.validators import MAX_QUERY_CHARS, validate_repo_payload


class ProjectExplainRequest(BaseModel):
    repo: Dict[str, Any]
    profile: Optional[Dict[str, Any]] = None
    query: Optional[str] = Field(default=None, max_length=MAX_QUERY_CHARS)

    @field_validator("repo")
    @classmethod
    def _check_repo(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        return validate_repo_payload(value)
