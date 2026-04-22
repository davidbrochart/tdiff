from subprocess import CalledProcessError

from anyio import Path, run_process


async def get_diff_paths(
    original: str = "", modified: str = "", cwd: str | None = None
) -> list[Path]:
    args = ""
    if original:
        args += original
    if modified:
        args += f" {modified}"
    result = await run_process(f"git diff --name-only {args}", cwd=cwd)
    paths = result.stdout.decode().splitlines()
    return [Path(path) for path in paths]


async def get_file_content(
    path: Path, ref: str = "", *, temp_path: Path | None = None, cwd: str | None = None
) -> str:
    content = ""
    if not ref:
        if cwd is None:
            _path = path
        else:
            _path = Path(cwd) / path
        try:
            content = await _path.read_text()
        except Exception:  # likely a unicode decode error
            content = f"Error loading file: {temp_path}"
    else:
        try:
            result = await run_process(f"git cat-file -p {ref}:{path}", cwd=cwd)
            content = result.stdout.decode()
        except CalledProcessError:  # the file likely doesn't exist
            content = ""
        except Exception:  # likely a unicode decode error
            content = f"Error loading file: {temp_path}"
    if (size := len(content)) > 100_000:
        content = f"File too big ({size} bytes): {temp_path}"
    return content
