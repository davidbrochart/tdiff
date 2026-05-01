from subprocess import CalledProcessError

from anyio import Path, create_task_group, run_process


async def get_dir_diff_paths(
    original: str = "", modified: str = "", cwd: str | None = None
) -> set[Path]:
    original_dir = Path(original)
    modified_dir = Path(modified)
    diff_paths: set[Path] = set()

    async with create_task_group() as tg:
        async for original_path in original_dir.rglob("*"):
            tg.start_soon(
                add_diff_path, original_path, original_dir, modified_dir, diff_paths
            )

        async for modified_path in modified_dir.rglob("*"):
            tg.start_soon(
                add_diff_path, modified_path, modified_dir, original_dir, diff_paths
            )

    return diff_paths


async def add_diff_path(
    original_path: Path, original_dir: Path, modified_dir: Path, diff_paths: set[Path]
) -> None:
    if original_path not in diff_paths and await original_path.is_file():
        relative_path = original_path.relative_to(original_dir)
        modified_path = modified_dir / relative_path
        if await modified_path.is_file():
            try:
                if await original_path.read_text() != await modified_path.read_text():
                    diff_paths.add(relative_path)
            except Exception:
                pass
        else:
            diff_paths.add(relative_path)


async def get_git_diff_paths(
    original: str = "", modified: str = "", cwd: str | None = None
) -> set[Path]:
    args = ""
    if original:
        args += original
    if modified:
        args += f" {modified}"
    result = await run_process(f"git diff --name-only {args}", cwd=cwd)
    paths = result.stdout.decode().splitlines()
    return set(Path(path) for path in paths)


async def get_file_content(path: Path, *, cwd: str | None = None) -> str:
    content = ""
    if cwd is None:
        _path = path
    else:
        _path = Path(cwd) / path
    try:
        content = await _path.read_text()
    except FileNotFoundError:
        content = ""
    except Exception:  # likely a unicode decode error
        content = f"Error loading file: {path}"
    if (size := len(content)) > 100_000:
        content = f"File too big ({size} bytes): {path}"
    return content


async def get_git_file_content(
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
        except FileNotFoundError:
            content = ""
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
