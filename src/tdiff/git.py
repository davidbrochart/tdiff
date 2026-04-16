from anyio import Path
from dulwich.object_store import tree_lookup_path
from dulwich.porcelain import status
from dulwich.repo import Repo


def get_unstaged_files(repo: Repo) -> list[Path]:
    _status = status(repo)
    return [Path(path.decode()) for path in _status.unstaged]


def get_committed_file(repo: Repo, path: Path) -> str:
    head_commit = repo[repo.head()]
    mode, sha = tree_lookup_path(repo.get_object, head_commit.tree, bytes(path))  # type: ignore
    blob = repo[sha]
    return blob.data.decode()  # type: ignore
