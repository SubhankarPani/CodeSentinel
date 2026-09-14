from github import Github

from app.config import GITHUB_TOKEN


class GitHubClient:
    """Handles communication with the GitHub API."""

    def __init__(self):
        self.github = Github(GITHUB_TOKEN)

    def get_repository(self, repository_name: str):
        """Return a GitHub repository."""
        return self.github.get_repo(repository_name)

    def get_pull_request(
        self,
        repository_name: str,
        pull_number: int
    ):
        """Return a specific pull request."""
        repository = self.get_repository(repository_name)
        return repository.get_pull(pull_number)

    def get_pull_request_files(
        self,
        repository_name: str,
        pull_number: int
    ):
        """Return files changed in a pull request."""
        pull_request = self.get_pull_request(
            repository_name,
            pull_number
        )

        return pull_request.get_files()

