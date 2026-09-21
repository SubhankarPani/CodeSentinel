import uuid

from fastapi import FastAPI, HTTPException, BackgroundTasks
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
        "http://127.0.0.1:5173",
        "https://codesentinel-ai-blush.vercel.app",
        "https://codesentinel-nmg28xegl-subhankar-panis-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# In-memory job storage
# --------------------------------

review_jobs = {}


# --------------------------------
# Request model
# --------------------------------

class ReviewRequest(BaseModel):
    repository: str
    pull_number: int


# --------------------------------
# Basic endpoints
# --------------------------------

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


# --------------------------------
# Background review
# --------------------------------

def run_review_job(
    job_id: str,
    repository: str,
    pull_number: int
):
    try:

        review_jobs[job_id]["status"] = "fetching_pr"

        github_client = GitHubClient()

        print(
            f"Fetching PR #{pull_number} "
            f"from {repository}..."
        )

        files = list(
            github_client.get_pull_request_files(
                repository,
                pull_number
            )
        )

        if not files:
            review_jobs[job_id]["status"] = "failed"
            review_jobs[job_id]["error"] = (
                "No changed files found in the Pull Request."
            )
            return

        print(f"Files changed: {len(files)}")


        # --------------------------------
        # Build code diff
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
        # Run review
        # --------------------------------

        review_jobs[job_id]["status"] = "reviewing"

        print("\nStarting CodeSentinel review...")

        def update_job_status(status):
            review_jobs[job_id]["status"] = status


        review_service = ReviewService(
            progress_callback=update_job_status
        )

        reviews = review_service.review(code_diff)

        if "final" not in reviews:

            review_jobs[job_id]["status"] = "failed"
            review_jobs[job_id]["error"] = (
                "CodeSentinel could not generate a final review."
            )
            return

        final_review = reviews["final"]


        # --------------------------------
        # Format GitHub comment
        # --------------------------------

        github_comment = format_review_as_markdown(
            final_review
        )


        # --------------------------------
        # Post GitHub comment
        # --------------------------------

        comment_url = None

        if POST_TO_GITHUB:

            print("\nPosting review to GitHub...")

            comment = github_client.post_pull_request_comment(
                repository,
                pull_number,
                github_comment
            )

            comment_url = comment.html_url

            print("✅ Review posted successfully!")


        # --------------------------------
        # Save result
        # --------------------------------

        review_jobs[job_id]["status"] = "completed"

        review_jobs[job_id]["result"] = {
            "status": "success",
            "repository": repository,
            "pull_number": pull_number,
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


    except Exception as error:

        print(
            f"\n❌ CodeSentinel error: {error}"
        )

        review_jobs[job_id]["status"] = "failed"

        review_jobs[job_id]["error"] = str(error)


# --------------------------------
# Start review
# --------------------------------

@app.post("/review")
def start_review(
    request: ReviewRequest,
    background_tasks: BackgroundTasks
):

    job_id = str(uuid.uuid4())

    review_jobs[job_id] = {
        "status": "queued",
        "result": None,
        "error": None
    }

    background_tasks.add_task(
        run_review_job,
        job_id,
        request.repository,
        request.pull_number
    )

    return {
        "status": "started",
        "job_id": job_id,
        "message": "CodeSentinel review started."
    }


# --------------------------------
# Check review status
# --------------------------------

@app.get("/review/{job_id}")
def get_review_status(job_id: str):

    if job_id not in review_jobs:

        raise HTTPException(
            status_code=404,
            detail="Review job not found."
        )

    job = review_jobs[job_id]

    response = {
        "job_id": job_id,
        "status": job["status"]
    }

    if job["status"] == "completed":
        response["result"] = job["result"]

    if job["status"] == "failed":
        response["error"] = job["error"]

    return response