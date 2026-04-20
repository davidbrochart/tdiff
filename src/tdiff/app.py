from asyncio import create_task

from anyio import Event, Path, TemporaryDirectory, create_task_group
from dulwich.repo import Repo
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive, var
from textual.widgets import DirectoryTree, Footer, Header
from textual import widgets

from textual_diff_view import DiffView, LoadError

from .git import get_committed_files, get_unstaged_paths


class GitDiffApp(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ("q", "quit", "Quit"),
        ("space", "toggle('split')", "Toggle split"),
        ("a", "toggle('annotations')", "Toggle annotations"),
        ("w", "toggle('wrap')", "Toggle wrap"),
    ]

    show_tree = var(True)
    path: reactive[Path | None] = reactive(None)
    split = var(True)
    annotations = var(True)
    wrap = var(True)

    def __init__(self, commit: str | None) -> None:
        self.commit = commit
        super().__init__()

    def watch_show_tree(self, show_tree: bool) -> None:
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        self.title = "tdiff"
        yield Header()
        with Container():
            yield VerticalScroll(id="tree-view")
            yield VerticalScroll(id="diff-view")
        yield Footer()

    async def _create_file(self, unstaged_path: Path, commited_file: str) -> None:
        path = self._temp_dir / unstaged_path
        await path.parent.mkdir(parents=True, exist_ok=True)
        await path.write_text(commited_file)

    async def _start(self) -> None:
        async with TemporaryDirectory() as self._temp_dir:
            self._started.set()
            await self._stopped.wait()

    async def on_mount(self) -> None:
        self._diff_view: DiffView | None = None
        self._started = Event()
        self._stopped = Event()
        self._task = create_task(self._start())
        await self._started.wait()
        self._repo = Repo(".")
        async with create_task_group() as tg:
            unstaged_paths = get_unstaged_paths(self._repo)
            commited_files = get_committed_files(
                self._repo, unstaged_paths, self.commit
            )
            for unstaged_path, commited_file in zip(unstaged_paths, commited_files):
                tg.start_soon(self._create_file, unstaged_path, commited_file)
        directory_tree = DirectoryTree(self._temp_dir)
        directory_tree.show_root = False
        await self.query_one("#tree-view").mount(directory_tree)
        directory_tree.focus()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        event.stop()
        self.path = event.path  # type: ignore

    async def watch_path(self, path: Path | None) -> None:
        diff_view = self.query_one("#diff-view")
        if path is None:
            return

        try:
            modified = path.relative_to(self._temp_dir)
            _diff_view = await DiffView.load(
                path,
                modified,
                split=self.split,
                annotations=self.annotations,
                wrap=self.wrap,
            )
        except LoadError as error:
            self.notify(str(error), title="Failed to load code", severity="error")
            self.sub_title = "ERROR"
        else:
            _diff_view.data_bind(
                GitDiffApp.split, GitDiffApp.annotations, GitDiffApp.wrap
            )
            if self._diff_view is not None:
                self._diff_view.remove()
            self._diff_view = _diff_view
            await diff_view.mount(_diff_view)
            self.sub_title = modified  # type: ignore

    def action_toggle_files(self) -> None:
        self.show_tree = not self.show_tree


class DiffApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("space", "toggle('split')", "Toggle split"),
        ("a", "toggle('annotations')", "Toggle annotations"),
        ("w", "toggle('wrap')", "Toggle wrap"),
    ]

    split = var(True)
    annotations = var(True)
    wrap = var(True)

    def __init__(self, original: str, modified: str) -> None:
        self.original = original
        self.modified = modified
        super().__init__()

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="diff-container")
        yield widgets.Footer()

    async def on_mount(self) -> None:
        try:
            diff_view = await DiffView.load(
                self.original,
                self.modified,
                split=self.split,
                annotations=self.annotations,
                wrap=self.wrap,
            )
        except LoadError as error:
            self.notify(str(error), title="Failed to load code", severity="error")
        else:
            diff_view.data_bind(DiffApp.split, DiffApp.annotations, DiffApp.wrap)
            await self.query_one("#diff-container").mount(diff_view)
