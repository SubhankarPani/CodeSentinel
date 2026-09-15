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

    final_review = reviews["final"]

    print("\n================================")
    print("       CODESENTINEL REVIEW")
    print("================================")

    if not final_review.issues:
        print("\nNo significant issues found.")
        return

    print(f"\nFound {len(final_review.issues)} issue(s).")

    for index, issue in enumerate(final_review.issues, start=1):
        print(f"\nIssue {index}")
        print(f"Severity: {issue.severity}")
        print(f"Category: {issue.category}")
        print(f"File: {issue.file}")
        print(f"Line: {issue.line}")
        print(f"\nDescription:")
        print(issue.description)
        print(f"\nRecommendation:")
        print(issue.recommendation)

        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()