from app.github.client import GitHubClient
from app.agents.style_agent import StyleAgent


def main():
    github_client = GitHubClient()

    repository_name = "psf/requests"
    pull_number = 7000

    print("Fetching Pull Request...")

    files = github_client.get_pull_request_files(
        repository_name,
        pull_number
    )

    # Combine all file diffs into one string
    code_diff = ""

    for file in files:
        code_diff += f"\n\nFile: {file.filename}\n"
        code_diff += f"Status: {file.status}\n"
        code_diff += f"Additions: {file.additions}\n"
        code_diff += f"Deletions: {file.deletions}\n"
        code_diff += "\n--- Diff ---\n"
        code_diff += file.patch or "No patch available."

    print("Pull Request retrieved successfully!")
    print(f"Files changed: {len(list(files))}")

    print("\nSending code to Style Agent...")

    style_agent = StyleAgent()

    review = style_agent.review(code_diff)

    print("\n================================")
    print("       CODESENTINEL REVIEW")
    print("================================")

    print("\n--- STYLE REVIEW ---")
    print(review)


if __name__ == "__main__":
    main()