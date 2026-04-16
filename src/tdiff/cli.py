from cyclopts import App

from .app import DiffApp, GitDiffApp

app = App()


@app.default
def default_action(
    path1: str | None = None,
    path2: str | None = None,
) -> None:
    if path1 is None and path2 is None:
        git_diff_app = GitDiffApp()
        git_diff_app.run()
    else:
        if path1 is None or path2 is None:
            raise RuntimeError("Either two paths must be provided, or none")
        diff_app = DiffApp(path1, path2)
        diff_app.run()
