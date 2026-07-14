"""Shared API error handling — log details server-side, return generic messages to clients."""

from __future__ import annotations

import logging

from fastapi import HTTPException

logger = logging.getLogger(__name__)

GENERIC_500 = "An internal server error occurred."
GENERIC_404 = "The requested resource was not found."


def raise_not_found(exc: Exception) -> None:
    logger.warning("Not found: %s", exc)
    raise HTTPException(status_code=404, detail=GENERIC_404) from exc


def raise_server_error(exc: Exception) -> None:
    logger.exception("Unhandled API error: %s", exc)
    raise HTTPException(status_code=500, detail=GENERIC_500) from exc
