"""Request payload guards for advisor / explainer endpoints."""

from __future__ import annotations

from typing import Any, Dict, List

MAX_README_CHARS = 100_000
MAX_STRING_FIELD_CHARS = 10_000
MAX_TOPICS = 100
MAX_RESULTS_ITEMS = 50
MAX_QUERY_CHARS = 500


def _string_len(value: Any) -> int:
    return len(value) if isinstance(value, str) else 0


def validate_repo_payload(repo: Dict[str, Any], *, field_name: str = "repo") -> Dict[str, Any]:
    if not isinstance(repo, dict):
        raise ValueError(f"{field_name} must be an object")

    readme_len = max(
        _string_len(repo.get("readme")),
        _string_len(repo.get("README")),
        _string_len(repo.get("readme_text")),
    )
    if readme_len > MAX_README_CHARS:
        raise ValueError(f"{field_name}.readme exceeds {MAX_README_CHARS} characters")

    for key, value in repo.items():
        if isinstance(value, str) and len(value) > MAX_STRING_FIELD_CHARS:
            raise ValueError(f"{field_name}.{key} exceeds {MAX_STRING_FIELD_CHARS} characters")

        if key in ("topics", "tags", "topic_list") and isinstance(value, list):
            if len(value) > MAX_TOPICS:
                raise ValueError(f"{field_name}.{key} exceeds {MAX_TOPICS} items")

    return repo


def validate_results_list(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if len(results) > MAX_RESULTS_ITEMS:
        raise ValueError(f"results exceeds {MAX_RESULTS_ITEMS} items")

    for idx, item in enumerate(results):
        if isinstance(item, dict) and "repo" in item and isinstance(item["repo"], dict):
            validate_repo_payload(item["repo"], field_name=f"results[{idx}].repo")
        elif isinstance(item, dict):
            validate_repo_payload(item, field_name=f"results[{idx}]")

    return results
