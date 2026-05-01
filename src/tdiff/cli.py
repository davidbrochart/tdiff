from pathlib import Path

from cyclopts import App

from .app import DiffApp, FileDiffApp

app = App()


@app.command
def git(
    original: str = "",
    modified: str = "",
) -> None:
    """Compare a git repository using similar parameters as the git CLI.

    Args:
        original: The original reference to compare, if any.
        modified: The modified reference to compare, if any.
    """
    if not original:
        original = "HEAD"
    diff_app = DiffApp(original, modified, True)
    diff_app.run()


@app.default
def default_action(
    original: str,
    modified: str,
) -> None:
    """Compare two directories or two files.

    Args:
        original: The original directory or file to compare.
        modified: The modified directory or file to compare.
    """
    if Path(original).is_file() and Path(modified).is_file():
        file_diff_app = FileDiffApp(original, modified)
        file_diff_app.run()
    elif Path(original).is_dir() and Path(modified).is_dir():
        diff_app = DiffApp(original, modified)
        diff_app.run()
    else:
        print("Parameters must be two directories or two files")
