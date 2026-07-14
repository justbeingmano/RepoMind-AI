from fastapi import APIRouter

from backend.core.http_errors import raise_server_error
from backend.schemas.project_explainer import ProjectExplainRequest
from backend.core.project_explainer import explain_project

router = APIRouter(prefix="/api/project-explainer", tags=["Project Explainer"])


@router.post("/explain")
def explain_project_endpoint(request: ProjectExplainRequest):
    try:
        return explain_project(
            repo_data=request.repo,
            profile=request.profile,
            query=request.query,
        )
    except Exception as e:
        raise_server_error(e)
