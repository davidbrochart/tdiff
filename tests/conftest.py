from subprocess import CalledProcessError

import pytest
from anyio import run_process


@pytest.fixture
async def git_repo(tmp_path) -> None:
    try:
        await run_process("git init".split(), cwd=tmp_path)
        for i in range(100):
            (tmp_path / f"foo{i}.txt").write_text("Hello, World!")
        await run_process("git add .".split(), cwd=tmp_path)
        await run_process('git commit -m "First commit"', cwd=tmp_path)
    except CalledProcessError as exc:
        print(f"{exc=}")
        raise


@pytest.fixture
def git_repo_with_changes(git_repo, tmp_path) -> None:
    for i in range(100):
        (tmp_path / f"foo{i}.txt").write_text(f"Hello, World! I'm number {i}")
