from fastapi import APIRouter, HTTPException

from backend.core.http_errors import raise_not_found, raise_server_error
from backend.core.repo_sanitize import public_repo_summary
from backend.core.semantic_loader import load_semantic_hybrid
from repo_utils import is_github_repository, repository_docs


router = APIRouter(prefix="/repos", tags=["Repositories"])


@router.get("/")
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


@router.get("/filters/options")
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


@router.get("/details/{repo_identifier:path}")
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
