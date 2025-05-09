# Copyright (c) Microsoft. All rights reserved.


import httpx
from pydantic import BaseModel, Field

from semantic_kernel.functions.kernel_function_decorator import kernel_function

# region GitHub Models


class Repo(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="full_name")
    description: str | None = Field(default=None, alias="description")
    url: str = Field(..., alias="html_url")


class User(BaseModel):
    id: int = Field(..., alias="id")
    login: str = Field(..., alias="login")
    name: str | None = Field(default=None, alias="name")
    company: str | None = Field(default=None, alias="company")
    url: str = Field(..., alias="html_url")


class Label(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")
    description: str | None = Field(default=None, alias="description")


class Issue(BaseModel):
    id: int = Field(..., alias="id")
    number: int = Field(..., alias="number")
    url: str = Field(..., alias="html_url")
    title: str = Field(..., alias="title")
    state: str = Field(..., alias="state")
    labels: list[Label] = Field(..., alias="labels")
    when_created: str | None = Field(default=None, alias="created_at")
    when_closed: str | None = Field(default=None, alias="closed_at")


class IssueDetail(Issue):
    body: str | None = Field(default=None, alias="body")


# endregion


class GitHubSettings(BaseModel):
    base_url: str = "https://api.github.com"
    token: str


class GitHubPlugin:
    def __init__(self, settings: GitHubSettings):
        self.settings = settings

    @kernel_function
    async def get_user_profile(self) -> "User":
        async with self.create_client() as client:
            response = await self.make_request(client, "/user")
            return User(**response)

    @kernel_function
    async def get_repository(self, organization: str, repo: str) -> "Repo":
        async with self.create_client() as client:
            response = await self.make_request(client, f"/repos/{organization}/{repo}")
            return Repo(**response)

    @kernel_function
    async def get_issues(
        self,
        organization: str,
        repo: str,
        max_results: int | None = None,
        state: str = "",
        label: str = "",
        assignee: str = "",
    ) -> list["Issue"]:
        async with self.create_client() as client:
            path = f"/repos/{organization}/{repo}/issues?"
            path = self.build_query(path, "state", state)
            path = self.build_query(path, "assignee", assignee)
            path = self.build_query(path, "labels", label)
            path = self.build_query(path, "per_page", str(max_results) if max_results else "")
            response = await self.make_request(client, path)
            return [Issue(**issue) for issue in response]
    
    @kernel_function
    async def get_commits(
        self,
        organization: str,
        repo: str,
        max_results: int | None = None,
        author: str = "",
        since: str = "",
        until: str = "",
    ) -> list[dict]:
        """
        Retrieve commits from a GitHub repository.

        Args:
            organization (str): The organization or user name.
            repo (str): The repository name.
            max_results (int, optional): Maximum number of commits to return.
            author (str, optional): Filter by commit author.
            since (str, optional): Only commits after this date (ISO 8601).
            until (str, optional): Only commits before this date (ISO 8601).

        Returns:
            list[dict]: A list of commit data dictionaries.
        """
        async with self.create_client() as client:
            path = f"/repos/{organization}/{repo}/commits?"
            path = self.build_query(path, "author", author)
            path = self.build_query(path, "since", since)
            path = self.build_query(path, "until", until)
            path = self.build_query(path, "per_page", str(max_results) if max_results else "")
            response = await self.make_request(client, path)
            return response
        
    @kernel_function
    async def get_commit_detail(
        self,
        organization: str,
        repo: str,
        commit_sha: str,
    ) -> dict:
        """
        Retrieve details for a specific commit in a GitHub repository.

        Args:
            organization (str): The organization or user name.
            repo (str): The repository name.
            commit_sha (str): The commit SHA.

        Returns:
            dict: The commit details.
        """
        async with self.create_client() as client:
            path = f"/repos/{organization}/{repo}/commits/{commit_sha}"
            response = await self.make_request(client, path)
            return response
        
    @kernel_function
    async def get_commit_diff(
        self,
        organization: str,
        repo: str,
        base_commit: str,
        head_commit: str,
    ) -> dict:
        """
        Retrieve the diff (code changes) between two commits in a GitHub repository.

        Args:
            organization (str): The organization or user name.
            repo (str): The repository name.
            base_commit (str): The base commit SHA.
            head_commit (str): The head commit SHA.

        Returns:
            dict: The comparison result including files changed, commits, and diff stats.
        """
        async with self.create_client() as client:
            path = f"/repos/{organization}/{repo}/compare/{base_commit}...{head_commit}"
            response = await self.make_request(client, path)
            return response
        
    @kernel_function
    async def create_git_issue_with_labels(
        self,
        organization: str,
        repo: str,
        title: str,
        body: str ,
        labels: list[str]
    ) -> dict:
        """
        Create a new issue with dummy text and labels in the specified repository.

        Args:
            organization (str): The organization or user name.
            repo (str): The repository name.
            title (str, optional): The title of the issue.
            body (str, optional): The body content of the issue.
            labels (list[str], optional): List of labels to assign.

        Returns:
            dict: The created issue details.
        """
        async with self.create_client() as client:
            path = f"/repos/{organization}/{repo}/issues"
            payload = {"title": title, "body": body, "labels": labels}
            print(f"POST REQUEST: {path}\nPayload: {payload}")
            response = await client.post(path, json=payload)
            response.raise_for_status()
            return response.json()

    @kernel_function
    async def get_issue_detail(self, organization: str, repo: str, issue_id: int) -> "IssueDetail":
        async with self.create_client() as client:
            path = f"/repos/{organization}/{repo}/issues/{issue_id}"
            response = await self.make_request(client, path)
            return IssueDetail(**response)

    def create_client(self) -> httpx.AsyncClient:
        headers = {
            "User-Agent": "request",
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.settings.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        return httpx.AsyncClient(base_url=self.settings.base_url, headers=headers, timeout=5)

    @staticmethod
    def build_query(path: str, key: str, value: str) -> str:
        if value:
            return f"{path}{key}={value}&"
        return path

    @staticmethod
    async def make_request(client: httpx.AsyncClient, path: str) -> dict:
        print(f"REQUEST: {path}\n")
        response = await client.get(path)
        response.raise_for_status()
        return response.json()