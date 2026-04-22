import pytest

from anyio import Path
from tdiff.git import get_diff_paths, get_file_content

pytestmark = pytest.mark.anyio


async def test_git(git_repo_with_changes, tmp_path):
    diff_paths = await get_diff_paths(cwd=tmp_path)
    assert set(diff_paths) == set([Path(f"foo{i}.txt") for i in range(100)])

    file_content0 = await get_file_content(diff_paths[0], cwd=tmp_path)
    assert file_content0 == "Hello, World! I'm number 0"
