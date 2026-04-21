from subprocess import CalledProcessError

from anyio import Path, create_task_group, run_process


async def get_diff_paths(
    original: str = "", modified: str = "", cwd: str | None = None
) -> list[Path]:
    args = ""
    if original:
        args += original
    if modified:
        args += f":{modified}"
    result = await run_process(f"git diff --name-only {args}", cwd=cwd)
    paths = result.stdout.decode().splitlines()
    return [Path(path) for path in paths]


async def get_file_contents(
    paths: list[Path], ref: str = "", cwd: str | None = None
) -> list[str]:
    contents = ["" for _ in paths]
    async with create_task_group() as tg:
        for i, path in enumerate(paths):
            tg.start_soon(get_file_content, path, ref, cwd, contents, i)
    return contents


async def get_file_content(
    path: Path, ref: str, cwd: str | None, contents: list[str | None], i: int
) -> None:
    if not ref:
        if cwd is None:
            _path = path
        else:
            _path = Path(cwd) / path
        content = await _path.read_text()
    else:
        try:
            result = await run_process(f"git cat-file -p {ref}:{path}", cwd=cwd)
            content = result.stdout.decode()
        except CalledProcessError:
            content = ""
    contents[i] = content
