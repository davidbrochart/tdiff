import pytest

from anyio import Path
from tdiff.utils import get_git_diff_paths, get_git_file_content

pytestmark = pytest.mark.anyio


async def test_git(git_repo_with_changes, tmp_path):
    diff_paths = await get_git_diff_paths(cwd=tmp_path)
    assert diff_paths == set([Path(f"foo{i}.txt") for i in range(100)])

    file_contents = set(
        [
            await get_git_file_content(diff_path, cwd=tmp_path)
            for diff_path in diff_paths
        ]
    )
    assert file_contents == set(f"Hello, World! I'm number {i}" for i in range(100))
