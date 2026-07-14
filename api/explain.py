from fastapi import APIRouter

from core.http_errors import raise_not_found, raise_server_error
from core.semantic_loader import explain_result, profile_from_payload
from core.project_explainer import explain_project

from api.schemas.search_schema import ExplainRequest
from api.schemas.project_explainer import ProjectExplainRequest

search_explain_router = APIRouter(prefix="/search", tags=["Search"])
project_explain_router = APIRouter(prefix="/api/project-explainer", tags=["Project Explainer"])


@search_explain_router.post("/explain")
def explain_search_result(request: ExplainRequest):
    try:
        profile = profile_from_payload(
            request.profile.model_dump() if request.profile else None
        )

        return explain_result(
            query=request.query,
            repo_identifier=request.repo_identifier,
            profile=profile,
        )

    except ValueError as e:
        raise_not_found(e)

    except Exception as e:
        raise_server_error(e)


@project_explain_router.post("/explain")
def explain_project_endpoint(request: ProjectExplainRequest):
    try:
        return explain_project(
            repo_data=request.repo,
            profile=request.profile,
            query=request.query,
        )
    except Exception as e:
        raise_server_error(e)
