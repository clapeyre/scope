from random import randint
from dataclasses import dataclass
from pathlib import Path
from rich.text import Text
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.containers import ScrollableContainer, Grid
from textual.widgets import (
    Button,
    Footer,
    Header,
    Static,
    Label,
    DataTable,
    DirectoryTree,
)

base_path = Path("/scratch/group/user")
jobs = [
    ("Job Id", "Folder", "Submission time"),
    (
        randint(100000, 200000),
        base_path / "RUNFOLDER1",
        randint(1000, 10000),
    ),
    (
        randint(100000, 200000),
        base_path / "RUNFOLDER2",
        randint(1000, 10000),
    ),
    (
        randint(100000, 200000),
        base_path / "RUNFOLDER3",
        randint(1000, 10000),
    ),
    (
        randint(100000, 200000),
        base_path / "RUNFOLDER4",
        randint(1000, 10000),
    ),
]


class QuitScreen(ModalScreen[bool]):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)


class TestApp(App):
    """A Textual app to manage stuff."""

    CSS_PATH = "test_tui.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "request_quit", "Quit")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield DataTable()
        yield DirectoryTree("./")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*jobs[0])
        for row in jobs[1:]:
            # Adding styled and justified `Text` objects instead of plain strings.
            styled_row = [
                Text(str(cell), style="italic #03AC13", justify="right") for cell in row
            ]
            table.add_row(*styled_row)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""

        def check_quit(quit: bool) -> None:
            """Called when QuitScreen is dismissed."""
            if quit:
                self.exit()

        self.push_screen(QuitScreen(), check_quit)


if __name__ == "__main__":
    app = TestApp()
    app.run()
