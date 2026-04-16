from tdiff.git import get_committed_file, get_unstaged_files


def test_git(git_repo_with_changes):
    repo = git_repo_with_changes
    unstaged_files = get_unstaged_files(repo)
    path = unstaged_files[0]
    committed_file = get_committed_file(repo, path)
    assert committed_file == "Hello, World!"
