from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import POST_TO_GITHUB
from app.github.client import GitHubClient
from app.github.formatter import format_review_as_markdown
from app.services.review_service import ReviewService


app = FastAPI(
    title="CodeSentinel",
    description="Autonomous AI-powered GitHub Pull Request Code Review",
    version="1.0.0"
)


# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReviewRequest(BaseModel):
    repository: str
    pull_number: int


@app.get("/")
def root():
    return {
        "message": "CodeSentinel API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/review")
def review_pull_request(request: ReviewRequest):

    try:
        # --------------------------------
        # 1. Fetch Pull Request
        # --------------------------------

        github_client = GitHubClient()

        print(
            f"Fetching PR #{request.pull_number} "
            f"from {request.repository}..."
        )

        files = list(
            github_client.get_pull_request_files(
                request.repository,
                request.pull_number
            )
        )

        if not files:
            raise HTTPException(
                status_code=400,
                detail="No changed files found in the Pull Request."
            )

        print(f"Files changed: {len(files)}")


        # --------------------------------
        # 2. Build code diff
        # --------------------------------

        code_diff = ""

        for file in files:

            code_diff += f"\n\nFile: {file.filename}\n"
            code_diff += f"Status: {file.status}\n"
            code_diff += f"Additions: {file.additions}\n"
            code_diff += f"Deletions: {file.deletions}\n"
            code_diff += "\n--- Diff ---\n"
            code_diff += file.patch or "No patch available."


        # --------------------------------
        # 3. Run CodeSentinel
        # --------------------------------

        print("\nStarting CodeSentinel review...")

        review_service = ReviewService()

        reviews = review_service.review(code_diff)

        if "final" not in reviews:
            raise HTTPException(
                status_code=500,
                detail="CodeSentinel could not generate a final review."
            )

        final_review = reviews["final"]


        # --------------------------------
        # 4. Format GitHub comment
        # --------------------------------

        github_comment = format_review_as_markdown(
            final_review
        )


        # --------------------------------
        # 5. Post to GitHub if enabled
        # --------------------------------

        comment_url = None

        if POST_TO_GITHUB:

            print("\nPosting review to GitHub...")

            comment = github_client.post_pull_request_comment(
                request.repository,
                request.pull_number,
                github_comment
            )

            comment_url = comment.html_url

            print("✅ Review posted successfully!")

        else:

            print("\n⚠️ POST_TO_GITHUB is disabled.")
            print("Review will not be posted to GitHub.")


        # --------------------------------
        # 6. Return response
        # --------------------------------

        return {
            "status": "success",
            "repository": request.repository,
            "pull_number": request.pull_number,
            "issues_found": len(final_review.issues),
            "comment_url": comment_url,

            "agents": {
                "style": reviews["style"].model_dump(),
                "logic": reviews["logic"].model_dump(),
                "security": reviews["security"].model_dump(),
                "final": reviews["final"].model_dump()
            },

            "review": final_review.model_dump()
        }


    except HTTPException:
        raise


    except Exception as error:

        print(
            f"\n❌ CodeSentinel error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )