#!/usr/bin/env python3

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll, Grid
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Static,
    TabbedContent,
    TabPane,
)

DEFAULT_FILE = "/home/coolkid75/Scholarship-Website/public/data/scholarships.json"


class SavePromptModal(ModalScreen[bool]):
    """Modal dialog asking whether to keep editing or quit after saving."""

    CSS = """
    SavePromptModal {
        align: center middle;
    }

    #dialog {
        padding: 2 4;
        width: 50;
        height: 11;
        border: round $accent;
        background: $surface;
    }

    #dialog-label {
        text-align: center;
        margin-bottom: 2;
    }

    #dialog-buttons {
        align: center middle;
    }

    Button {
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Label("Successfully saved!\nWhat would you like to do next?", id="dialog-label")
            with Horizontal(id="dialog-buttons"):
                yield Button("Keep Editing", id="edit", variant="primary")
                yield Button("Quit", id="quit", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)


class ScholarshipEditor(App):
    """Terminal-based multi-page scholarship JSON editor."""

    TITLE = "Scholarship Manager"

    CSS = """
    Screen {
        layout: vertical;
    }

    TabbedContent {
        height: 1fr;
    }

    TabPane {
        padding: 1 2;
    }

    .field-label {
        margin-top: 1;
        color: $text-muted;
    }

    Input {
        margin-bottom: 1;
    }

    .button-row {
        height: auto;
        margin-top: 1;
        margin-bottom: 1;
    }

    #status {
        height: 2;
        color: $success;
        padding-left: 1;
    }

    #preview {
        border: round $accent;
        height: 10;
        padding: 1;
        overflow-y: auto;
    }

    ListView {
        height: 1fr;
        border: round $accent;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        ("ctrl+l", "load_file", "Load JSON"),
        ("ctrl+s", "save_file", "Save JSON"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.scholarships = []
        self.current_index = None
        self.file_path = Path(DEFAULT_FILE)

    def compose(self) -> ComposeResult:
        yield Header()

        with TabbedContent(id="tabs"):
            # Page 1: View & Select List
            with TabPane("View & Select", id="tab-view"):
                yield Label("Select a scholarship to edit or delete:", classes="field-label")
                yield ListView(id="scholarship-list")
                yield Label("JSON File Path", classes="field-label")
                yield Input(value=str(self.file_path), id="file-input")
                yield Static("Use Ctrl+L to load and Ctrl+S to save.", id="status-view")

            # Page 2: Add New Scholarship
            with TabPane("Add New", id="tab-add"):
                with VerticalScroll():
                    yield Label("Name", classes="field-label")
                    yield Input(id="add-name")
                    yield Label("Amount", classes="field-label")
                    yield Input(id="add-amount", placeholder="Example: $5,000 or Varies")
                    yield Label("Amount Value", classes="field-label")
                    yield Input(id="add-amountValue", placeholder="Example: 5000")
                    yield Label("Deadline", classes="field-label")
                    yield Input(id="add-deadline", placeholder="Example: January 31, 2026")
                    yield Label("Badge", classes="field-label")
                    yield Input(id="add-badge", placeholder="Example: Jan 31")
                    yield Label("Description", classes="field-label")
                    yield Input(id="add-description")
                    yield Label("Eligibility", classes="field-label")
                    yield Input(id="add-eligibility")
                    yield Label("Search Keywords", classes="field-label")
                    yield Input(id="add-search", placeholder="Example: engineering STEM scholarship")
                    yield Label("Page", classes="field-label")
                    yield Input(id="add-page", placeholder="Example: scholarship-name.html")
                    
                    with Horizontal(classes="button-row"):
                        yield Button("Add Scholarship", id="btn-add", variant="success")

            # Page 3: Edit / Delete Scholarship
            with TabPane("Edit / Delete", id="tab-edit"):
                with VerticalScroll():
                    yield Label("Editing Selected Scholarship", classes="field-label")
                    yield Label("Name", classes="field-label")
                    yield Input(id="edit-name")
                    yield Label("Amount", classes="field-label")
                    yield Input(id="edit-amount")
                    yield Label("Amount Value", classes="field-label")
                    yield Input(id="edit-amountValue")
                    yield Label("Deadline", classes="field-label")
                    yield Input(id="edit-deadline")
                    yield Label("Badge", classes="field-label")
                    yield Input(id="edit-badge")
                    yield Label("Description", classes="field-label")
                    yield Input(id="edit-description")
                    yield Label("Eligibility", classes="field-label")
                    yield Input(id="edit-eligibility")
                    yield Label("Search Keywords", classes="field-label")
                    yield Input(id="edit-search")
                    yield Label("Page", classes="field-label")
                    yield Input(id="edit-page")

                    with Horizontal(classes="button-row"):
                        yield Button("Update", id="btn-update", variant="warning")
                        yield Button("Delete", id="btn-delete", variant="error")

                    yield Label("Live JSON Preview", classes="field-label")
                    yield Static("", id="preview")

        yield Static("Ready.", id="status")
        yield Footer()

    def on_mount(self):
        self.load_file()

    # ---------------------------------------------------------
    # Helpers & Validation
    # ---------------------------------------------------------

    def get_form_data(self, prefix: str):
        return {
            "name": self.query_one(f"#{prefix}-name", Input).value.strip(),
            "amount": self.query_one(f"#{prefix}-amount", Input).value.strip(),
            "amountValue": self.query_one(f"#{prefix}-amountValue", Input).value.strip(),
            "deadline": self.query_one(f"#{prefix}-deadline", Input).value.strip(),
            "badge": self.query_one(f"#{prefix}-badge", Input).value.strip(),
            "description": self.query_one(f"#{prefix}-description", Input).value.strip(),
            "eligibility": self.query_one(f"#{prefix}-eligibility", Input).value.strip(),
            "search": self.query_one(f"#{prefix}-search", Input).value.strip(),
            "page": self.query_one(f"#{prefix}-page", Input).value.strip(),
        }

    def set_form_data(self, prefix: str, data: dict):
        for field in ["name", "amount", "amountValue", "deadline", "badge", "description", "eligibility", "search", "page"]:
            self.query_one(f"#{prefix}-{field}", Input).value = str(data.get(field, ""))

    def set_status(self, message, error=False):
        status = self.query_one("#status", Static)
        if error:
            status.update(f"[bold red]{message}[/bold red]")
        else:
            status.update(f"[green]{message}[/green]")

    def validate_form(self, data):
        required = ["name", "amount", "deadline", "description", "eligibility", "search", "page"]
        missing = [f for f in required if not data[f]]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"
        if data["amountValue"]:
            try:
                int(data["amountValue"])
            except ValueError:
                return False, "Amount Value must be a whole number."
        return True, ""

    def convert_data_types(self, data):
        val = data["amountValue"]
        data["amountValue"] = int(val) if val else 0
        return data

    @staticmethod
    def make_badge(deadline):
        for fmt in ["%B %d, %Y", "%b %d, %Y"]:
            try:
                date = datetime.strptime(deadline, fmt)
                return date.strftime("%b %-d")
            except ValueError:
                continue
        return deadline

    # ---------------------------------------------------------
    # File Operations (Keybind Actions)
    # ---------------------------------------------------------

    def action_load_file(self):
        self.load_file()

    def load_file(self):
        file_input = self.query_one("#file-input", Input)
        self.file_path = Path(file_input.value if file_input.value else DEFAULT_FILE)

        if not self.file_path.exists():
            self.scholarships = []
            self.refresh_list()
            self.set_status(f"{self.file_path} does not exist. Starting empty.")
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON root must be a list.")
            self.scholarships = data
            self.current_index = None
            self.refresh_list()
            self.set_status(f"Loaded {len(self.scholarships)} scholarships from {self.file_path.name}")
        except Exception as e:
            self.set_status(f"Could not load JSON: {e}", error=True)

    def action_save_file(self):
        try:
            if self.file_path.exists():
                backup = self.file_path.with_suffix(self.file_path.suffix + ".bak")
                shutil.copy2(self.file_path, backup)

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.scholarships, f, indent=2, ensure_ascii=False)
                f.write("\n")

            self.set_status(f"Saved {len(self.scholarships)} scholarships successfully!")
            
            # Prompt user after save: Keep editing or Quit?
            def check_modal(should_quit: bool | None):
                if should_quit:
                    self.exit()

            self.push_screen(SavePromptModal(), check_modal)

        except Exception as e:
            self.set_status(f"Could not save file: {e}", error=True)

    # ---------------------------------------------------------
    # List and Tab Management
    # ---------------------------------------------------------

    def refresh_list(self):
        list_view = self.query_one("#scholarship-list", ListView)
        list_view.clear()
        for idx, sch in enumerate(self.scholarships):
            name = sch.get("name", "Unnamed")
            deadline = sch.get("deadline", "No deadline")
            amount = sch.get("amount", "N/A")
            text = f"[bold]{name}[/bold]\n[dim]Deadline: {deadline} | Amount: {amount}[/dim]"
            list_view.append(ListItem(Label(text)))

    def on_list_view_selected(self, event: ListView.Selected):
        index = event.list_view.index
        if index is not None and 0 <= index < len(self.scholarships):
            self.current_index = index
            sch = self.scholarships[index]
            self.set_form_data("edit", sch)
            self.update_preview()
            # Switch to the Edit/Delete tab automatically
            self.query_one("#tabs", TabbedContent).active = "tab-edit"
            self.set_status(f"Loaded scholarship #{index + 1} for editing.")

    def update_preview(self):
        try:
            data = self.get_form_data("edit")
            preview_str = json.dumps(data, indent=2, ensure_ascii=False)
            self.query_one("#preview", Static).update(preview_str)
        except Exception:
            pass

    def on_input_changed(self, event: Input.Changed):
        if "edit-" in event.input.id:
            self.update_preview()

    # ---------------------------------------------------------
    # Button Actions
    # ---------------------------------------------------------

    def on_button_pressed(self, event: Button.Pressed):
        btn_id = event.button.id

        if btn_id == "btn-add":
            data = self.get_form_data("add")
            valid, err = self.validate_form(data)
            if not valid:
                self.set_status(err, error=True)
                return
            data = self.convert_data_types(data)
            if not data["badge"]:
                data["badge"] = self.make_badge(data["deadline"])

            self.scholarships.append(data)
            self.refresh_list()
            # Clear add form inputs
            for field in ["name", "amount", "amountValue", "deadline", "badge", "description", "eligibility", "search", "page"]:
                self.query_one(f"#add-{field}", Input).value = ""
            
            # Switch back to view tab
            self.query_one("#tabs", TabbedContent).active = "tab-view"
            self.set_status("Scholarship added! Press Ctrl+S to save.")

        elif btn_id == "btn-update":
            if self.current_index is None:
                self.set_status("No scholarship selected.", error=True)
                return
            data = self.get_form_data("edit")
            valid, err = self.validate_form(data)
            if not valid:
                self.set_status(err, error=True)
                return
            data = self.convert_data_types(data)
            if not data["badge"]:
                data["badge"] = self.make_badge(data["deadline"])

            self.scholarships[self.current_index] = data
            self.refresh_list()
            self.query_one("#tabs", TabbedContent).active = "tab-view"
            self.set_status("Scholarship updated! Press Ctrl+S to save.")

        elif btn_id == "btn-delete":
            if self.current_index is None:
                self.set_status("No scholarship selected.", error=True)
                return
            deleted = self.scholarships.pop(self.current_index)
            self.current_index = None
            self.refresh_list()
            self.query_one("#tabs", TabbedContent).active = "tab-view"
            self.set_status(f"Deleted: {deleted.get('name', 'Unnamed')}. Press Ctrl+S to save.")


if __name__ == "__main__":
    ScholarshipEditor().run()
