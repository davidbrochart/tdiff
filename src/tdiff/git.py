from anyio import Path
from dulwich.object_store import tree_lookup_path
from dulwich.porcelain import status
from dulwich.repo import Repo


def get_unstaged_paths(repo: Repo) -> list[Path]:
    _status = status(repo)
    return [Path(path.decode()) for path in _status.unstaged]


def get_committed_files(
    repo: Repo, paths: list[Path], commit: str | None = None
) -> list[str]:
    commit_i = 0
    commit_id = b""
    if commit is not None:
        if (i := commit.find("~")) >= 0:
            commit_i = int(commit[i + 1 :])
            commit_id = commit[:i].encode()
        else:
            commit_id = commit.encode()
    for i, entry in enumerate(repo.get_walker()):
        _commit = entry.commit
        if _commit.id == commit_id:
            commit_i += i
            commit_id = b""
        if not commit_id and i == commit_i:
            break
    files = []
    for path in paths:
        mode, sha = tree_lookup_path(repo.get_object, _commit.tree, bytes(path))
        blob = repo[sha]
        files.append(blob.data.decode())  # type: ignore
    return files
