import pytest
from dulwich import porcelain


@pytest.fixture
def git_repo(tmp_path):
    repo = porcelain.init(tmp_path)
    (tmp_path / "foo.txt").write_text("Hello, World!")
    porcelain.add(repo, "foo.txt")
    porcelain.commit(repo, b"First commit")
    return repo


@pytest.fixture
def git_repo_with_changes(git_repo, tmp_path):
    (tmp_path / "foo.txt").write_text("hello world")
    return git_repo
