"""Strip bulky fields from repo documents returned by list/summary endpoints."""

from __future__ import annotations

from typing import Any, Dict, List

_README_KEYS = frozenset(
    {"readme", "README", "readme_text", "content", "processed_text", "tokens"}
)


def public_repo_summary(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Return a repo dict safe for list endpoints (no full README / token blobs)."""
    return {key: value for key, value in doc.items() if key not in _README_KEYS}
