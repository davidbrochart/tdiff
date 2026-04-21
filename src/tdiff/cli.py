from cyclopts import App

from .app import DiffApp, GitDiffApp

app = App()


@app.command
def git(
    original: str = "",
    modified: str = "",
) -> None:
    if not original:
        original = "HEAD"
    git_diff_app = GitDiffApp(original, modified)
    git_diff_app.run()


@app.default
def default_action(
    original: str,
    modified: str,
) -> None:
    diff_app = DiffApp(original, modified)
    diff_app.run()
