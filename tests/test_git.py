import pytest

from anyio import Path
from tdiff.git import get_diff_paths, get_file_contents

pytestmark = pytest.mark.anyio


async def test_git(git_repo_with_changes, tmp_path):
    diff_paths = await get_diff_paths(cwd=tmp_path)
    assert diff_paths == [Path("foo.txt")]

    file_contents = await get_file_contents(diff_paths, cwd=tmp_path)
    assert file_contents == ["hello world"]
