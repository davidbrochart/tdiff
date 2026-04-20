from tdiff.git import get_committed_files, get_unstaged_paths


def test_git(git_repo_with_changes):
    repo = git_repo_with_changes
    unstaged_paths = get_unstaged_paths(repo)
    committed_files = get_committed_files(repo, unstaged_paths)
    assert committed_files == ["Hello, World!"]
