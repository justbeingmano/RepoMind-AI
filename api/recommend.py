from fastapi import APIRouter, HTTPException

from core.http_errors import raise_not_found, raise_server_error
from core.profile_loader import (
    get_profile_questions_payload,
    recommend_for_profile,
    search_with_profile,
)
from core.repo_sanitize import public_repo_summary
from core.semantic_loader import load_semantic_hybrid, recommend_similar
from core.repo_utils import is_github_repository, repository_docs

from api.schemas.search_schema import RecommendRequest
from api.schemas.profile_schema import ProfileRecommendRequest, ProfileSearchRequest

# Routers
recommend_router = APIRouter(prefix="/recommend", tags=["Recommendation"])
profile_router = APIRouter(prefix="/profile", tags=["Profile"])
repos_router = APIRouter(prefix="/repos", tags=["Repositories"])

# --- Recommendation Endpoints ---
@recommend_router.post("/")
def recommend_similar_repositories(request: RecommendRequest):
    """Similar repos via semantic embeddings (semantic_hybrid_recommender)."""
    try:
        results = recommend_similar(
            repo_identifier=request.repo_identifier,
            top_k=request.top_k,
            same_language_only=request.same_language_only,
        )

        return {
            "repo_identifier": request.repo_identifier,
            "count": len(results),
            "engine": "semantic_hybrid_recommender",
            "results": results,
        }

    except ValueError as e:
        raise_not_found(e)

    except Exception as e:
        raise_server_error(e)


# --- Profile Endpoints ---
@profile_router.get("/questions")
def get_profile_questions():
    try:
        return get_profile_questions_payload()
    except Exception as e:
        raise_server_error(e)


@profile_router.post("/recommend")
def profile_recommend(request: ProfileRecommendRequest):
    try:
        payload = request.model_dump()
        results = recommend_for_profile(payload)
        return {
            "count": len(results),
            "engine": "smart_profile_recommender_v2",
            "profile": {
                k: v
                for k, v in payload.items()
                if k != "top_k" and v is not None
            },
            "results": results,
        }
    except Exception as e:
        raise_server_error(e)


@profile_router.post("/search")
def profile_search(request: ProfileSearchRequest):
    try:
        payload = request.model_dump()
        results = search_with_profile(payload)
        return {
            "query": request.query,
            "count": len(results),
            "results": results,
        }
    except Exception as e:
        raise_server_error(e)


# --- Repository Endpoints ---
@repos_router.get("/")
def list_repositories(limit: int = 20):
    try:
        hybrid = load_semantic_hybrid()
        limit = max(1, min(limit, 100))

        repos = [
            public_repo_summary(doc)
            for doc in repository_docs(hybrid.docs)
        ]
        return {
            "count": min(limit, len(repos)),
            "results": repos[:limit],
        }

    except Exception as e:
        raise_server_error(e)


@repos_router.get("/filters/options")
def get_filter_options():
    try:
        hybrid = load_semantic_hybrid()

        languages = set()
        licenses = set()
        topics = set()

        for repo in repository_docs(hybrid.docs):
            if repo.get("language"):
                languages.add(repo["language"])

            if repo.get("license"):
                licenses.add(repo["license"])

            for topic in repo.get("topics", []) or []:
                topics.add(topic)

        return {
            "languages": sorted(languages),
            "licenses": sorted(licenses),
            "topics": sorted(topics),
        }

    except Exception as e:
        raise_server_error(e)


@repos_router.get("/details/{repo_identifier:path}")
def get_repository(repo_identifier: str):
    try:
        hybrid = load_semantic_hybrid()
        idx = hybrid.find_repo_index(repo_identifier)

        if idx is None:
            raise HTTPException(status_code=404, detail="The requested resource was not found.")

        doc = hybrid.docs[idx]
        if not is_github_repository(doc):
            raise HTTPException(status_code=404, detail="The requested resource was not found.")

        return doc

    except HTTPException:
        raise

    except Exception as e:
        raise_server_error(e)
