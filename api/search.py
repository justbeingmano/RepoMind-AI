from fastapi import APIRouter

from core.http_errors import raise_server_error
from core.semantic_loader import hybrid_search
from api.schemas.search_schema import SearchRequest

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/")
def search_repositories(request: SearchRequest):
    try:
        payload = request.model_dump()
        results = hybrid_search(payload)

        return {
            "query": request.query,
            "count": len(results),
            "engine": "semantic_hybrid_recommender",
            "results": results,
        }

    except Exception as e:
        raise_server_error(e)
