from __future__ import annotations

from fastapi import APIRouter

from backend.core.ai_advisor import advise
from backend.core.http_errors import raise_server_error
from backend.core.repo_comparator import compare_repos
from backend.core.repo_explainer import explain_repo
from backend.core.roadmap_generator import generate_roadmap
from backend.schemas.advisor import (
    AdvisorSummaryRequest,
    CompareReposRequest,
    ExplainRepoRequest,
    RoadmapRequest,
)

router = APIRouter(prefix="/api/advisor", tags=["AI Advisor"])


@router.post("/explain")
def explain(request: ExplainRepoRequest):
    try:
        return explain_repo(
            repo=request.repo,
            profile=request.profile,
            query=request.query,
            score_breakdown=request.score_breakdown,
            include_roadmap=request.include_roadmap,
        )
    except Exception as e:
        raise_server_error(e)


@router.post("/roadmap")
def roadmap(request: RoadmapRequest):
    try:
        return generate_roadmap(repo=request.repo, profile=request.profile)
    except Exception as e:
        raise_server_error(e)


@router.post("/compare")
def compare(request: CompareReposRequest):
    try:
        return compare_repos(
            repo_a=request.repo_a,
            repo_b=request.repo_b,
            profile=request.profile,
            query=request.query,
        )
    except Exception as e:
        raise_server_error(e)


@router.post("/summary")
def summary(request: AdvisorSummaryRequest):
    try:
        return advise(
            query=request.query,
            profile=request.profile,
            results=request.results,
            top_k=request.top_k,
        )
    except Exception as e:
        raise_server_error(e)
