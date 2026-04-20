from cyclopts import App

from .app import DiffApp, GitDiffApp

app = App()


@app.command
def git(
    commit: str | None = None,
) -> None:
    git_diff_app = GitDiffApp(commit)
    git_diff_app.run()


@app.default
def default_action(
    path1: str,
    path2: str,
) -> None:
    diff_app = DiffApp(path1, path2)
    diff_app.run()
