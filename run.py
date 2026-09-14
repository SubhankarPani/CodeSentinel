from app.github.client import GitHubClient
from app.services.review_service import ReviewService


def main():
    github_client = GitHubClient()

    repository_name = "psf/requests"
    pull_number = 7000

    print("Fetching Pull Request...")

    files = list(
        github_client.get_pull_request_files(
            repository_name,
            pull_number
        )
    )

    print("Pull Request retrieved successfully!")
    print(f"Files changed: {len(files)}")

    # Combine all file diffs
    code_diff = ""

    for file in files:
        code_diff += f"\n\nFile: {file.filename}\n"
        code_diff += f"Status: {file.status}\n"
        code_diff += f"Additions: {file.additions}\n"
        code_diff += f"Deletions: {file.deletions}\n"
        code_diff += "\n--- Diff ---\n"
        code_diff += file.patch or "No patch available."

    print("\nStarting CodeSentinel review...")

    review_service = ReviewService()

    reviews = review_service.review(code_diff)

    print("\n================================")
    print("       CODESENTINEL REVIEW")
    print("================================")

    for review_type, review in reviews.items():

        print(f"\n--- {review_type.upper()} REVIEW ---")

        if not review.issues:
            print(f"No significant {review_type} issues found.")
            continue

        for index, issue in enumerate(review.issues, start=1):
            print(f"\nIssue {index}")
            print(f"Severity: {issue.severity}")
            print(f"Category: {issue.category}")
            print(f"File: {issue.file}")
            print(f"Line: {issue.line}")
            print(f"Description: {issue.description}")
            print(f"Recommendation: {issue.recommendation}")


if __name__ == "__main__":
    main()