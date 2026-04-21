from subprocess import CalledProcessError

import pytest
from anyio import run_process


@pytest.fixture
async def git_repo(tmp_path) -> None:
    (tmp_path / "foo.txt").write_text("Hello, World!")
    try:
        await run_process("git init".split(), cwd=tmp_path)
        await run_process("git add foo.txt".split(), cwd=tmp_path)
        await run_process('git commit -m "First commit"', cwd=tmp_path)
    except CalledProcessError as exc:
        print(f"{exc=}")
        raise


@pytest.fixture
def git_repo_with_changes(git_repo, tmp_path) -> None:
    (tmp_path / "foo.txt").write_text("hello world")
