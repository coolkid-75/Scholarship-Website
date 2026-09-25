#!/usr/bin/env python3

import html
import json
import re
import shutil
import tkinter as tk

from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


# =============================================================
# CONFIGURATION
# =============================================================

DEFAULT_FILE = (
    "/home/coolkid75/Scholarship-Website/"
    "public/data/scholarships.json"
)

# Directory where generated scholarship HTML pages are saved.
HTML_DIRECTORY = (
    "/home/coolkid75/Scholarship-Website/"
    "public/scholarships"
)

# Global GUI scale.
UI_SCALE = 1.5


# =============================================================
# HTML TEMPLATE
# =============================================================
#
# This is the template used for every generated scholarship page.
#
# The following values are populated automatically:
#
# {name}
# {amount}
# {deadline}
# {badge}
# {description}
# {eligibility_html}
# {application_url}
#
# You can edit the HTML/CSS below to change the design of all
# generated scholarship pages.
# =============================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>{name} | Pea Ridge Scholarship Hub</title>

    <link
        rel="stylesheet"
        href="../style.css"
    >

    <style>

        .detail-page {{
            min-height: 100vh;
            padding: 80px 0;
        }}

        .breadcrumb {{
            margin-bottom: 30px;

            color: var(--muted);

            font-size: .9rem;
        }}

        .breadcrumb a {{
            color: var(--teal);
            font-weight: 700;
        }}

        .scholarship-detail {{
            max-width: 850px;
            margin: auto;

            padding: 50px;

            background: white;

            border-radius: 25px;

            border:
                1px solid var(--border);

            box-shadow: var(--shadow);
        }}

        .detail-icon {{
            min-width: 75px;
            min-height: 75px;
            width: fit-content;

            display: inline-flex;
            align-items: center;
            justify-content: center;

            padding: 12px 18px;

            margin-bottom: 25px;

            border-radius: 20px;

            font-size: 2.2rem;
            line-height: 1;

            background:
                linear-gradient(
                    135deg,
                    rgba(24,166,166,.15),
                    rgba(18,63,112,.08)
                );

            box-sizing: border-box;
        }}


        .detail-label {{
            display: inline-block;

            padding: 7px 12px;

            margin-bottom: 15px;

            color: var(--navy);

            background:
                rgba(245,185,66,.2);

            border-radius: 8px;

            font-size: .8rem;

            font-weight: 900;
        }}

        .scholarship-detail h1 {{
            color: var(--navy);

            font-size:
                clamp(2rem, 5vw, 3.5rem);

            line-height: 1.05;

            letter-spacing: -.04em;

            margin-bottom: 20px;
        }}

        .detail-intro {{
            color: var(--muted);

            font-size: 1.1rem;

            margin-bottom: 35px;
        }}

        .detail-grid {{
            display: grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap: 15px;

            margin-bottom: 35px;
        }}

        .detail-stat {{
            padding: 20px;

            background: var(--off-white);

            border-radius: 15px;
        }}

        .detail-stat span {{
            display: block;

            color: var(--muted);

            font-size: .75rem;

            margin-bottom: 4px;
        }}

        .detail-stat strong {{
            color: var(--navy);

            font-size: 1.1rem;
        }}

        .detail-section {{
            margin-top: 35px;
        }}

        .detail-section h2 {{
            color: var(--navy);

            margin-bottom: 12px;
        }}

        .detail-section p {{
            color: var(--muted);
        }}

        .detail-actions {{
            display: flex;

            flex-wrap: wrap;

            gap: 12px;

            margin-top: 40px;
        }}

        .back-button {{
            display: inline-flex;

            align-items: center;

            padding: 14px 20px;

            color: var(--blue);

            border: 2px solid var(--blue);

            border-radius: 12px;

            font-weight: 800;
        }}

        @media (max-width: 600px) {{

            .scholarship-detail {{
                padding: 30px 22px;
            }}

            .detail-grid {{
                grid-template-columns: 1fr;
            }}

        }}

    </style>

</head>


<body>


<header class="site-header">

    <div class="container header-content">

        <a href="./" class="logo">
            <span class="logo-icon">🎓</span>
            <span>Pea Ridge Scholarship Hub</span>
        </a>

        <nav>

            <a href="./">
                Home
            </a>

            <a href="../scholarships.html">
                Scholarships
            </a>

            <a href="../tips.html">
                Tips
            </a>

            <a href="../contact.html">
                Contact
            </a>

        </nav>

    </div>

</header>


<main class="detail-page">

    <div class="container">

        <div class="breadcrumb">

            <a href="./">
                Home
            </a>

            &nbsp; / &nbsp;

            <a href="../scholarships.html">
                Scholarships
            </a>

            &nbsp; / &nbsp;

            {name}

        </div>


        <article class="scholarship-detail">

            <div class="detail-icon">
                {badge}
            </div>

            <span class="detail-label">
                SCHOLARSHIP OPPORTUNITY
            </span>

            <h1>
                {name}
            </h1>


            <div class="detail-grid">

                <div class="detail-stat">

                    <span>
                        Award
                    </span>

                    <strong>
                        {amount}
                    </strong>

                </div>


                <div class="detail-stat">

                    <span>
                        Deadline
                    </span>

                    <strong>
                        {deadline}
                    </strong>

                </div>

            </div>


            <div class="detail-section">

                <h2>
                    About This Scholarship
                </h2>

                <p>
                    {description}
                </p>

            </div>


            <div class="detail-section">

                <h2>
                    Eligibility
                </h2>

{eligibility_html}

            </div>


            <div class="detail-actions">

                <a
                    href="{application_url}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="cta-button"
                >
                    Visit Application →
                </a>

                <a
                    href="../scholarships.html"
                    class="back-button"
                >
                    ← Back to Scholarships
                </a>

            </div>

        </article>

    </div>

</main>


<footer>

    <div class="container footer-content">

        <div>

            <div class="footer-logo">
                🎓 Pea Ridge Scholarship Hub
            </div>

            <p>
                Helping students discover opportunities
                for their future.
            </p>

        </div>

    </div>


    <div class="container copyright">

        <p>
            © 2026 Pea Ridge Scholarship Hub.
        </p>

    </div>

</footer>


</body>

</html>
"""


# =============================================================
# APPLICATION
# =============================================================

class ScholarshipEditor(tk.Tk):
    """
    Scholarship JSON editor and HTML page generator.

    JSON data is stored in:
        /home/coolkid75/Scholarship-Website/public/data/

    Generated HTML pages are stored in:
        /home/coolkid75/Scholarship-Website/public/scholarships/
    """

    # =========================================================
    # Initialization
    # =========================================================

    def __init__(self):

        super().__init__()

        # -----------------------------------------------------
        # Tk scaling
        # -----------------------------------------------------

        self.tk.call(
            "tk",
            "scaling",
            UI_SCALE,
        )

        # -----------------------------------------------------
        # Window
        # -----------------------------------------------------

        self.title(
            "Scholarship Manager"
        )

        self.geometry(
            "1400x900"
        )

        self.minsize(
            1100,
            750,
        )

        # -----------------------------------------------------
        # Application state
        # -----------------------------------------------------

        self.scholarships = []

        self.current_index = None

        self.file_path = Path(
            DEFAULT_FILE
        )

        self.html_directory = Path(
            HTML_DIRECTORY
        )

        # -----------------------------------------------------
        # Create application
        # -----------------------------------------------------

        self._create_variables()
        self._create_styles()
        self._create_menu()
        self._create_gui()

        # -----------------------------------------------------
        # Default JSON path
        # -----------------------------------------------------

        self.file_var.set(
            str(self.file_path)
        )

        # -----------------------------------------------------
        # Load JSON shortly after GUI starts
        # -----------------------------------------------------

        self.after(
            100,
            self.load_file,
        )

    # =========================================================
    # Variables
    # =========================================================

    def _create_variables(self):

        self.file_var = tk.StringVar()

        self.add_vars = {
            "name": tk.StringVar(),
            "amount": tk.StringVar(),
            "amountValue": tk.StringVar(),
            "deadline": tk.StringVar(),
            "badge": tk.StringVar(),
            "description": tk.StringVar(),
            "eligibility": tk.StringVar(),
            "search": tk.StringVar(),
            "page": tk.StringVar(),
            "applicationUrl": tk.StringVar(),
        }

        self.edit_vars = {
            "name": tk.StringVar(),
            "amount": tk.StringVar(),
            "amountValue": tk.StringVar(),
            "deadline": tk.StringVar(),
            "badge": tk.StringVar(),
            "description": tk.StringVar(),
            "eligibility": tk.StringVar(),
            "search": tk.StringVar(),
            "page": tk.StringVar(),
            "applicationUrl": tk.StringVar(),
        }

        self.status_var = tk.StringVar(
            value="Ready."
        )

    # =========================================================
    # Styles
    # =========================================================

    def _create_styles(self):

        style = ttk.Style(self)

        try:
            style.theme_use(
                "clam"
            )
        except tk.TclError:
            pass

        # -----------------------------------------------------
        # Fonts
        # -----------------------------------------------------

        base_font = (
            "TkDefaultFont",
            13,
        )

        bold_font = (
            "TkDefaultFont",
            13,
            "bold",
        )

        title_font = (
            "TkDefaultFont",
            21,
            "bold",
        )

        section_font = (
            "TkDefaultFont",
            14,
            "bold",
        )

        button_font = (
            "TkDefaultFont",
            13,
            "bold",
        )

        heading_font = (
            "TkDefaultFont",
            13,
            "bold",
        )

        # -----------------------------------------------------
        # General
        # -----------------------------------------------------

        style.configure(
            ".",
            font=base_font,
        )

        style.configure(
            "TLabel",
            font=base_font,
        )

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        style.configure(
            "Title.TLabel",
            font=title_font,
        )

        style.configure(
            "Section.TLabel",
            font=section_font,
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        style.configure(
            "TButton",
            font=button_font,
            padding=(16, 10),
        )

        style.configure(
            "Accent.TButton",
            font=button_font,
            padding=(18, 11),
        )

        # -----------------------------------------------------
        # Entries
        # -----------------------------------------------------

        style.configure(
            "TEntry",
            font=base_font,
            padding=8,
        )

        # -----------------------------------------------------
        # Notebook
        # -----------------------------------------------------

        style.configure(
            "TNotebook",
            tabmargins=(4, 4, 4, 0),
        )

        style.configure(
            "TNotebook.Tab",
            font=bold_font,
            padding=(20, 12),
        )

        # -----------------------------------------------------
        # Treeview
        # -----------------------------------------------------

        style.configure(
            "Treeview",
            font=(
                "TkDefaultFont",
                13,
            ),
            rowheight=46,
        )

        style.configure(
            "Treeview.Heading",
            font=heading_font,
            padding=(10, 10),
        )

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        style.configure(
            "Status.TLabel",
            font=base_font,
            padding=(12, 9),
        )

        # -----------------------------------------------------
        # Label frames
        # -----------------------------------------------------

        style.configure(
            "TLabelframe.Label",
            font=heading_font,
        )

        # -----------------------------------------------------
        # Scrollbars
        # -----------------------------------------------------

        style.configure(
            "Vertical.TScrollbar",
            width=18,
        )

        style.configure(
            "Horizontal.TScrollbar",
            width=18,
        )

    # =========================================================
    # Menu
    # =========================================================

    def _create_menu(self):

        menu_font = (
            "TkDefaultFont",
            13,
        )

        menu_bar = tk.Menu(
            self,
            font=menu_font,
        )

        file_menu = tk.Menu(
            menu_bar,
            tearoff=False,
            font=menu_font,
        )

        file_menu.add_command(
            label="Load JSON",
            command=self.load_file,
            accelerator="Ctrl+L",
        )

        file_menu.add_command(
            label="Save JSON",
            command=self.save_file,
            accelerator="Ctrl+S",
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Generate All HTML Pages",
            command=self.generate_all_html,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Quit",
            command=self.destroy,
            accelerator="Ctrl+Q",
        )

        menu_bar.add_cascade(
            label="File",
            menu=file_menu,
        )

        self.config(
            menu=menu_bar
        )

        self.bind_all(
            "<Control-l>",
            lambda event: self.load_file(),
        )

        self.bind_all(
            "<Control-s>",
            lambda event: self.save_file(),
        )

        self.bind_all(
            "<Control-q>",
            lambda event: self.destroy(),
        )

    # =========================================================
    # Main GUI
    # =========================================================

    def _create_gui(self):

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = ttk.Frame(
            self,
            padding=(20, 18),
        )

        header.pack(
            fill="x",
        )

        ttk.Label(
            header,
            text="Scholarship Manager",
            style="Title.TLabel",
        ).pack(
            side="left",
        )

        ttk.Button(
            header,
            text="Generate HTML",
            command=self.generate_all_html,
        ).pack(
            side="right",
            padx=(8, 0),
        )

        ttk.Button(
            header,
            text="Load JSON",
            command=self.load_file,
        ).pack(
            side="right",
            padx=(8, 0),
        )

        ttk.Button(
            header,
            text="Save JSON",
            command=self.save_file,
            style="Accent.TButton",
        ).pack(
            side="right",
            padx=(8, 0),
        )

        # -----------------------------------------------------
        # Notebook
        # -----------------------------------------------------

        self.notebook = ttk.Notebook(
            self,
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15),
        )

        self.view_tab = ttk.Frame(
            self.notebook,
            padding=20,
        )

        self.add_tab = ttk.Frame(
            self.notebook,
            padding=20,
        )

        self.edit_tab = ttk.Frame(
            self.notebook,
            padding=20,
        )

        self.notebook.add(
            self.view_tab,
            text="View & Select",
        )

        self.notebook.add(
            self.add_tab,
            text="Add New",
        )

        self.notebook.add(
            self.edit_tab,
            text="Edit / Delete",
        )

        self._create_view_tab()
        self._create_add_tab()
        self._create_edit_tab()

        # -----------------------------------------------------
        # Status bar
        # -----------------------------------------------------

        status_frame = ttk.Frame(
            self,
        )

        status_frame.pack(
            fill="x",
            side="bottom",
        )

        ttk.Separator(
            status_frame,
            orient="horizontal",
        ).pack(
            fill="x",
        )

        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            style="Status.TLabel",
        )

        self.status_label.pack(
            fill="x",
        )

    # =========================================================
    # View Tab
    # =========================================================

    def _create_view_tab(self):

        ttk.Label(
            self.view_tab,
            text="Select a scholarship to edit or delete:",
            style="Section.TLabel",
        ).pack(
            anchor="w",
            pady=(0, 12),
        )

        # -----------------------------------------------------
        # Tree
        # -----------------------------------------------------

        tree_frame = ttk.Frame(
            self.view_tab,
        )

        tree_frame.pack(
            fill="both",
            expand=True,
        )

        columns = (
            "name",
            "deadline",
            "amount",
        )

        self.scholarship_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.scholarship_tree.heading(
            "name",
            text="Scholarship",
        )

        self.scholarship_tree.heading(
            "deadline",
            text="Deadline",
        )

        self.scholarship_tree.heading(
            "amount",
            text="Amount",
        )

        self.scholarship_tree.column(
            "name",
            width=600,
            minwidth=300,
            anchor="w",
        )

        self.scholarship_tree.column(
            "deadline",
            width=250,
            minwidth=180,
            anchor="w",
        )

        self.scholarship_tree.column(
            "amount",
            width=220,
            minwidth=150,
            anchor="w",
        )

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.scholarship_tree.yview,
        )

        self.scholarship_tree.configure(
            yscrollcommand=scrollbar.set,
        )

        self.scholarship_tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.scholarship_tree.bind(
            "<<TreeviewSelect>>",
            self.on_tree_select,
        )

        self.scholarship_tree.bind(
            "<Double-1>",
            self.on_tree_double_click,
        )

        # -----------------------------------------------------
        # JSON path
        # -----------------------------------------------------

        path_frame = ttk.Frame(
            self.view_tab,
        )

        path_frame.pack(
            fill="x",
            pady=(18, 0),
        )

        ttk.Label(
            path_frame,
            text="JSON File Path:",
            font=(
                "TkDefaultFont",
                13,
                "bold",
            ),
        ).pack(
            side="left",
            padx=(0, 10),
        )

        ttk.Entry(
            path_frame,
            textvariable=self.file_var,
        ).pack(
            side="left",
            fill="x",
            expand=True,
            ipady=4,
        )

        ttk.Button(
            path_frame,
            text="Browse...",
            command=self.browse_file,
        ).pack(
            side="left",
            padx=(10, 0),
        )

    # =========================================================
    # Add Tab
    # =========================================================

    def _create_add_tab(self):

        self.add_form = self._create_form(
            self.add_tab,
            self.add_vars,
            include_buttons=True,
            button_callback=self.add_scholarship,
            button_text="Add Scholarship",
        )

    # =========================================================
    # Edit Tab
    # =========================================================

    def _create_edit_tab(self):

        outer = ttk.Frame(
            self.edit_tab,
        )

        outer.pack(
            fill="both",
            expand=True,
        )

        # -----------------------------------------------------
        # Left side
        # -----------------------------------------------------

        form_container = ttk.Frame(
            outer,
        )

        form_container.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15),
        )

        self.edit_form = self._create_form(
            form_container,
            self.edit_vars,
            include_buttons=False,
        )

        # -----------------------------------------------------
        # Edit buttons
        # -----------------------------------------------------

        button_frame = ttk.Frame(
            form_container,
        )

        button_frame.pack(
            fill="x",
            pady=(18, 12),
        )

        ttk.Button(
            button_frame,
            text="Update",
            command=self.update_scholarship,
        ).pack(
            side="left",
            padx=(0, 10),
        )

        ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_scholarship,
        ).pack(
            side="left",
        )

        # -----------------------------------------------------
        # Right side JSON preview
        # -----------------------------------------------------

        preview_container = ttk.LabelFrame(
            outer,
            text="Live JSON Preview",
            padding=12,
        )

        preview_container.pack(
            side="right",
            fill="both",
            expand=True,
        )

        self.preview_text = tk.Text(
            preview_container,
            wrap="none",
            font=(
                "TkFixedFont",
                13,
            ),
            background="#111111",
            foreground="#eeeeee",
            insertbackground="white",
            padx=12,
            pady=12,
        )

        self.preview_text.pack(
            fill="both",
            expand=True,
        )

        preview_scroll = ttk.Scrollbar(
            preview_container,
            orient="vertical",
            command=self.preview_text.yview,
        )

        preview_scroll.pack(
            side="right",
            fill="y",
        )

        self.preview_text.configure(
            yscrollcommand=preview_scroll.set,
        )

        # -----------------------------------------------------
        # Live preview updates
        # -----------------------------------------------------

        for variable in self.edit_vars.values():

            variable.trace_add(
                "write",
                self.update_preview,
            )

    # =========================================================
    # Generic Form
    # =========================================================

    def _create_form(
        self,
        parent,
        variables,
        include_buttons=False,
        button_callback=None,
        button_text=None,
    ):

        # -----------------------------------------------------
        # Canvas
        # -----------------------------------------------------

        canvas = tk.Canvas(
            parent,
            highlightthickness=0,
        )

        scrollbar = ttk.Scrollbar(
            parent,
            orient="vertical",
            command=canvas.yview,
        )

        form = ttk.Frame(
            canvas,
        )

        window_id = canvas.create_window(
            (0, 0),
            window=form,
            anchor="nw",
        )

        canvas.configure(
            yscrollcommand=scrollbar.set,
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        def update_scroll_region(
            event=None,
        ):

            canvas.configure(
                scrollregion=canvas.bbox("all"),
            )

        def resize_form(event):

            canvas.itemconfigure(
                window_id,
                width=event.width,
            )

        form.bind(
            "<Configure>",
            update_scroll_region,
        )

        canvas.bind(
            "<Configure>",
            resize_form,
        )

        # -----------------------------------------------------
        # Fields
        # -----------------------------------------------------

        fields = [
            (
                "name",
                "Name",
                "",
            ),
            (
                "amount",
                "Amount",
                "$5,000 or Varies",
            ),
            (
                "amountValue",
                "Amount Value",
                "5000",
            ),
            (
                "deadline",
                "Deadline",
                "September 30, 2026",
            ),
            (
                "badge",
                "Badge / Icon",
                "🎖️",
            ),
            (
                "description",
                "Description",
                "",
            ),
            (
                "eligibility",
                "Eligibility",
                "1. First requirement\n2. Second requirement",
            ),
            (
                "search",
                "Search Keywords",
                "engineering STEM scholarship",
            ),
            (
                "page",
                "Page",
                "scholarship-name.html",
            ),
            (
                "applicationUrl",
                "Application URL",
                "https://example.com/apply",
            ),
        ]

        for key, label, placeholder in fields:

            ttk.Label(
                form,
                text=label,
                font=(
                    "TkDefaultFont",
                    13,
                    "bold",
                ),
            ).pack(
                anchor="w",
                pady=(12, 5),
            )

            entry = ttk.Entry(
                form,
                textvariable=variables[key],
                font=(
                    "TkDefaultFont",
                    13,
                ),
            )

            entry.pack(
                fill="x",
                ipady=7,
            )

            prefix = (
                "add"
                if variables is self.add_vars
                else "edit"
            )

            setattr(
                self,
                f"{prefix}_{key}_entry",
                entry,
            )

        # -----------------------------------------------------
        # Add button
        # -----------------------------------------------------

        if include_buttons and button_callback:

            button_frame = ttk.Frame(
                form,
            )

            button_frame.pack(
                fill="x",
                pady=(25, 15),
            )

            ttk.Button(
                button_frame,
                text=button_text,
                command=button_callback,
                style="Accent.TButton",
            ).pack(
                side="left",
            )

        return form

    # =========================================================
    # Form Helpers
    # =========================================================

    def get_form_data(
        self,
        variables,
    ):

        return {
            "name": variables["name"].get().strip(),
            "amount": variables["amount"].get().strip(),
            "amountValue": variables["amountValue"].get().strip(),
            "deadline": variables["deadline"].get().strip(),
            "badge": variables["badge"].get().strip(),
            "description": variables["description"].get().strip(),
            "eligibility": variables["eligibility"].get().strip(),
            "search": variables["search"].get().strip(),
            "page": variables["page"].get().strip(),
            "applicationUrl": variables[
                "applicationUrl"
            ].get().strip(),
        }

    def set_form_data(
        self,
        variables,
        data,
    ):

        fields = [
            "name",
            "amount",
            "amountValue",
            "deadline",
            "badge",
            "description",
            "eligibility",
            "search",
            "page",
            "applicationUrl",
        ]

        for field in fields:

            variables[field].set(
                str(
                    data.get(
                        field,
                        "",
                    )
                )
            )

    def clear_form(
        self,
        variables,
    ):

        for variable in variables.values():
            variable.set("")

    # =========================================================
    # Validation
    # =========================================================

    def validate_form(
        self,
        data,
    ):

        required = [
            "name",
            "amount",
            "deadline",
            "description",
            "eligibility",
            "search",
            "page",
            "applicationUrl",
        ]

        missing = [
            field
            for field in required
            if not data[field]
        ]

        if missing:

            return (
                False,
                "Missing required fields: "
                + ", ".join(missing),
            )

        # -----------------------------------------------------
        # Amount value
        # -----------------------------------------------------

        if data["amountValue"]:

            try:

                int(
                    data["amountValue"]
                )

            except ValueError:

                return (
                    False,
                    "Amount Value must be a whole number.",
                )

        # -----------------------------------------------------
        # URL
        # -----------------------------------------------------

        if not (
            data["applicationUrl"].startswith(
                "http://"
            )
            or data["applicationUrl"].startswith(
                "https://"
            )
        ):

            return (
                False,
                "Application URL must start with "
                "http:// or https://",
            )

        return True, ""

    # =========================================================
    # Data Type Conversion
    # =========================================================

    def convert_data_types(
        self,
        data,
    ):

        value = data["amountValue"]

        data["amountValue"] = (
            int(value)
            if value
            else 0
        )

        return data

    # =========================================================
    # Badge Helper
    # =========================================================

    @staticmethod
    def make_badge(
        deadline,
    ):

        formats = [
            "%B %d, %Y",
            "%b %d, %Y",
        ]

        for fmt in formats:

            try:

                date = datetime.strptime(
                    deadline,
                    fmt,
                )

                try:

                    return date.strftime(
                        "%b %-d"
                    )

                except ValueError:

                    return date.strftime(
                        "%b %#d"
                    )

            except ValueError:

                continue

        return "🎖️"

    # =========================================================
    # HTML Helpers
    # =========================================================

    @staticmethod
    def escape_html(
        value,
    ):
        """
        Safely escape user-entered text before inserting it
        into HTML.
        """

        return html.escape(
            str(value),
            quote=True,
        )

    # ---------------------------------------------------------
    # Eligibility
    # ---------------------------------------------------------

    @staticmethod
    def format_eligibility(
        eligibility,
    ):
        """
        Convert eligibility text into HTML paragraphs.

        Example input:

            1. First requirement
            2. Second requirement
            3. Third requirement

        becomes separate HTML paragraphs.

        Blank lines are ignored.
        """

        if not eligibility:

            return ""

        lines = eligibility.splitlines()

        paragraphs = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            escaped = (
                ScholarshipEditor.escape_html(
                    line
                )
            )

            paragraphs.append(
                "                <p>\n"
                f"                    {escaped}\n"
                "                </p>"
            )

        return "\n\n".join(
            paragraphs
        )

    # ---------------------------------------------------------
    # Filename
    # ---------------------------------------------------------

    @staticmethod
    def clean_filename(
        filename,
    ):
        """
        Convert a supplied page name into a safe .html filename.
        """

        filename = str(
            filename
        ).strip()

        if not filename:
            return ""

        # -----------------------------------------------------
        # Remove directory separators.
        # -----------------------------------------------------

        filename = filename.replace(
            "/",
            "",
        )

        filename = filename.replace(
            "\\",
            "",
        )

        # -----------------------------------------------------
        # Remove .html extension.
        # -----------------------------------------------------

        if filename.lower().endswith(
            ".html"
        ):

            filename = filename[:-5]

        # -----------------------------------------------------
        # Replace unsafe characters.
        # -----------------------------------------------------

        filename = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "-",
            filename,
        )

        filename = filename.strip(
            "-"
        )

        if not filename:

            return ""

        return (
            filename
            + ".html"
        )

    # ---------------------------------------------------------
    # Determine HTML filename
    # ---------------------------------------------------------

    def get_html_filename(
        self,
        scholarship,
    ):
        """
        Use the page field if supplied.

        Otherwise generate a filename from the scholarship name.
        """

        page = scholarship.get(
            "page",
            "",
        )

        filename = (
            self.clean_filename(
                page
            )
        )

        if filename:

            return filename

        name = scholarship.get(
            "name",
            "scholarship",
        )

        generated = re.sub(
            r"[^a-zA-Z0-9]+",
            "-",
            name.lower(),
        )

        generated = generated.strip(
            "-"
        )

        if not generated:

            generated = "scholarship"

        return (
            generated
            + ".html"
        )

    # =========================================================
    # Generate HTML
    # =========================================================

    def generate_html(
        self,
        scholarship,
    ):
        """
        Populate the HTML template using scholarship data.
        """

        # -----------------------------------------------------
        # Basic fields
        # -----------------------------------------------------

        name = self.escape_html(
            scholarship.get(
                "name",
                "Scholarship Opportunity",
            )
        )

        amount = self.escape_html(
            scholarship.get(
                "amount",
                "Varies",
            )
        )

        deadline = self.escape_html(
            scholarship.get(
                "deadline",
                "No deadline listed",
            )
        )

        badge = self.escape_html(
            scholarship.get(
                "badge",
                "🎖️",
            )
        )

        description = self.escape_html(
            scholarship.get(
                "description",
                "",
            )
        )

        application_url = self.escape_html(
            scholarship.get(
                "applicationUrl",
                "#",
            )
        )

        # -----------------------------------------------------
        # Eligibility
        # -----------------------------------------------------

        eligibility_html = (
            self.format_eligibility(
                scholarship.get(
                    "eligibility",
                    "",
                )
            )
        )

        # -----------------------------------------------------
        # Populate template
        #
        # NOTE:
        # The HTML_TEMPLATE uses doubled braces for CSS
        # because it is a Python format string.
        # -----------------------------------------------------

        html_content = HTML_TEMPLATE.format(
            name=name,
            amount=amount,
            deadline=deadline,
            badge=badge,
            description=description,
            eligibility_html=eligibility_html,
            application_url=application_url,
        )

        return html_content

    # =========================================================
    # Generate One HTML Page
    # =========================================================

    def generate_html_for_scholarship(
        self,
        scholarship,
    ):
        """
        Generate one HTML file for one scholarship.
        """

        try:

            # -------------------------------------------------
            # Create output directory.
            # -------------------------------------------------

            self.html_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            # -------------------------------------------------
            # Determine filename.
            # -------------------------------------------------

            filename = (
                self.get_html_filename(
                    scholarship
                )
            )

            output_path = (
                self.html_directory
                / filename
            )

            # -------------------------------------------------
            # Generate content.
            # -------------------------------------------------

            content = (
                self.generate_html(
                    scholarship
                )
            )

            # -------------------------------------------------
            # Write file.
            # -------------------------------------------------

            with open(
                output_path,
                "w",
                encoding="utf-8",
            ) as file:

                file.write(
                    content
                )

            return output_path

        except Exception as exc:

            raise RuntimeError(
                "Could not generate HTML for "
                f"'{scholarship.get('name', 'Unnamed')}': "
                f"{exc}"
            )

    # =========================================================
    # Generate All HTML
    # =========================================================

    def generate_all_html(
        self,
        show_message=True,
    ):
        """
        Generate HTML pages for every scholarship.
        """

        if not self.scholarships:

            self.set_status(
                "There are no scholarships to generate.",
                error=True,
            )

            if show_message:

                messagebox.showwarning(
                    "No Scholarships",
                    "There are no scholarships to generate.",
                )

            return False

        try:

            # -------------------------------------------------
            # Create directory.
            # -------------------------------------------------

            self.html_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            generated = []

            # -------------------------------------------------
            # Generate each page.
            # -------------------------------------------------

            for scholarship in self.scholarships:

                output_path = (
                    self.generate_html_for_scholarship(
                        scholarship
                    )
                )

                generated.append(
                    output_path
                )

            # -------------------------------------------------
            # Status.
            # -------------------------------------------------

            self.set_status(
                f"Generated {len(generated)} "
                "HTML scholarship pages."
            )

            # -------------------------------------------------
            # Message.
            # -------------------------------------------------

            if show_message:

                messagebox.showinfo(
                    "HTML Generated",
                    f"Successfully generated "
                    f"{len(generated)} scholarship page(s).\n\n"
                    f"Location:\n"
                    f"{self.html_directory}",
                )

            return True

        except Exception as exc:

            self.set_status(
                f"HTML generation failed: {exc}",
                error=True,
            )

            messagebox.showerror(
                "HTML Generation Error",
                str(exc),
            )

            return False

    # =========================================================
    # Status
    # =========================================================

    def set_status(
        self,
        message,
        error=False,
    ):

        self.status_var.set(
            message
        )

        try:

            self.status_label.configure(
                foreground=(
                    "#d32f2f"
                    if error
                    else "#2e7d32"
                )
            )

        except tk.TclError:
            pass

    # =========================================================
    # File Browser
    # =========================================================

    def browse_file(self):

        filename = (
            filedialog.askopenfilename(
                title="Select Scholarship JSON",
                initialdir=str(
                    self.file_path.parent
                    if self.file_path.parent.exists()
                    else Path.home()
                ),
                filetypes=[
                    (
                        "JSON files",
                        "*.json",
                    ),
                    (
                        "All files",
                        "*.*",
                    ),
                ],
            )
        )

        if filename:

            self.file_var.set(
                filename
            )

            self.load_file()

    # =========================================================
    # Load JSON
    # =========================================================

    def load_file(self):

        path_string = (
            self.file_var.get().strip()
        )

        self.file_path = Path(
            path_string
            if path_string
            else DEFAULT_FILE
        )

        # -----------------------------------------------------
        # File doesn't exist.
        # -----------------------------------------------------

        if not self.file_path.exists():

            self.scholarships = []

            self.current_index = None

            self.refresh_list()

            self.clear_form(
                self.edit_vars
            )

            self.update_preview()

            self.set_status(
                f"{self.file_path} does not exist. "
                "Starting empty."
            )

            return

        # -----------------------------------------------------
        # Load JSON.
        # -----------------------------------------------------

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(
                    file
                )

            # -------------------------------------------------
            # JSON must contain a list.
            # -------------------------------------------------

            if not isinstance(
                data,
                list,
            ):

                raise ValueError(
                    "JSON root must be a list."
                )

            self.scholarships = data

            self.current_index = None

            self.refresh_list()

            self.clear_form(
                self.edit_vars
            )

            self.update_preview()

            self.set_status(
                f"Loaded {len(self.scholarships)} "
                "scholarships from "
                f"{self.file_path.name}"
            )

        except Exception as exc:

            self.set_status(
                f"Could not load JSON: {exc}",
                error=True,
            )

            messagebox.showerror(
                "Load Error",
                "Could not load JSON:\n\n"
                f"{exc}",
            )

    # =========================================================
    # Save JSON
    # =========================================================

    def save_file(self):

        try:

            # -------------------------------------------------
            # Create JSON directory.
            # -------------------------------------------------

            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            # -------------------------------------------------
            # Backup current JSON.
            # -------------------------------------------------

            if self.file_path.exists():

                backup = (
                    self.file_path.with_suffix(
                        self.file_path.suffix
                        + ".bak"
                    )
                )

                shutil.copy2(
                    self.file_path,
                    backup,
                )

            # -------------------------------------------------
            # Write JSON.
            # -------------------------------------------------

            with open(
                self.file_path,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    self.scholarships,
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

                file.write(
                    "\n"
                )

            # -------------------------------------------------
            # Generate HTML.
            # -------------------------------------------------

            html_success = (
                self.generate_all_html(
                    show_message=False
                )
            )

            if html_success:

                self.set_status(
                    f"Saved {len(self.scholarships)} "
                    "scholarships and generated "
                    "HTML pages successfully!"
                )

            else:

                self.set_status(
                    f"Saved {len(self.scholarships)} "
                    "scholarships, but HTML generation "
                    "failed.",
                    error=True,
                )

            # -------------------------------------------------
            # Show save dialog.
            # -------------------------------------------------

            self.show_save_prompt()

        except Exception as exc:

            self.set_status(
                f"Could not save file: {exc}",
                error=True,
            )

            messagebox.showerror(
                "Save Error",
                "Could not save file:\n\n"
                f"{exc}",
            )

    # =========================================================
    # Save Confirmation
    # =========================================================

    def show_save_prompt(self):

        dialog = tk.Toplevel(
            self
        )

        dialog.title(
            "Successfully Saved"
        )

        dialog.geometry(
            "560x250"
        )

        dialog.resizable(
            False,
            False,
        )

        dialog.transient(
            self
        )

        dialog.grab_set()

        # -----------------------------------------------------
        # Center dialog
        # -----------------------------------------------------

        self.update_idletasks()

        dialog_width = 560
        dialog_height = 250

        x = (
            self.winfo_x()
            + (
                self.winfo_width()
                - dialog_width
            )
            // 2
        )

        y = (
            self.winfo_y()
            + (
                self.winfo_height()
                - dialog_height
            )
            // 2
        )

        dialog.geometry(
            f"{dialog_width}x{dialog_height}+{x}+{y}"
        )

        # -----------------------------------------------------
        # Contents
        # -----------------------------------------------------

        frame = ttk.Frame(
            dialog,
            padding=30,
        )

        frame.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            frame,
            text="Successfully saved!",
            font=(
                "TkDefaultFont",
                17,
                "bold",
            ),
        ).pack(
            pady=(0, 10)
        )

        ttk.Label(
            frame,
            text=(
                "JSON saved and scholarship HTML pages "
                "generated successfully."
            ),
            font=(
                "TkDefaultFont",
                13,
            ),
        ).pack(
            pady=(0, 25)
        )

        ttk.Label(
            frame,
            text="What would you like to do next?",
            font=(
                "TkDefaultFont",
                13,
            ),
        ).pack(
            pady=(0, 15)
        )

        buttons = ttk.Frame(
            frame
        )

        buttons.pack()

        def keep_editing():

            dialog.grab_release()
            dialog.destroy()

        def quit_app():

            dialog.grab_release()
            dialog.destroy()
            self.destroy()

        ttk.Button(
            buttons,
            text="Keep Editing",
            command=keep_editing,
        ).pack(
            side="left",
            padx=6,
        )

        ttk.Button(
            buttons,
            text="Quit",
            command=quit_app,
        ).pack(
            side="left",
            padx=6,
        )

        dialog.protocol(
            "WM_DELETE_WINDOW",
            keep_editing,
        )

    # =========================================================
    # List Management
    # =========================================================

    def refresh_list(self):

        # -----------------------------------------------------
        # Clear existing rows.
        # -----------------------------------------------------

        for item in (
            self.scholarship_tree.get_children()
        ):

            self.scholarship_tree.delete(
                item
            )

        # -----------------------------------------------------
        # Add scholarships.
        # -----------------------------------------------------

        for index, scholarship in enumerate(
            self.scholarships
        ):

            name = scholarship.get(
                "name",
                "Unnamed",
            )

            deadline = scholarship.get(
                "deadline",
                "No deadline",
            )

            amount = scholarship.get(
                "amount",
                "N/A",
            )

            self.scholarship_tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    name,
                    deadline,
                    amount,
                ),
            )

    # =========================================================
    # Tree Selection
    # =========================================================

    def on_tree_select(
        self,
        event=None,
    ):

        selection = (
            self.scholarship_tree.selection()
        )

        if not selection:
            return

        try:

            index = int(
                selection[0]
            )

        except ValueError:

            return

        if not (
            0 <= index < len(
                self.scholarships
            )
        ):

            return

        self.current_index = index

        scholarship = (
            self.scholarships[index]
        )

        self.set_form_data(
            self.edit_vars,
            scholarship,
        )

        self.update_preview()

        self.notebook.select(
            self.edit_tab
        )

        self.set_status(
            f"Loaded scholarship #{index + 1} "
            "for editing."
        )

    def on_tree_double_click(
        self,
        event=None,
    ):

        self.on_tree_select()

    # =========================================================
    # JSON Preview
    # =========================================================

    def update_preview(
        self,
        *args,
    ):

        try:

            data = self.get_form_data(
                self.edit_vars
            )

            preview = json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )

            self.preview_text.delete(
                "1.0",
                tk.END,
            )

            self.preview_text.insert(
                "1.0",
                preview,
            )

        except Exception:

            pass

    # =========================================================
    # Add Scholarship
    # =========================================================

    def add_scholarship(self):

        data = self.get_form_data(
            self.add_vars
        )

        # -----------------------------------------------------
        # Validate.
        # -----------------------------------------------------

        valid, error = (
            self.validate_form(
                data
            )
        )

        if not valid:

            self.set_status(
                error,
                error=True,
            )

            messagebox.showwarning(
                "Invalid Scholarship",
                error,
            )

            return

        # -----------------------------------------------------
        # Convert amountValue.
        # -----------------------------------------------------

        data = (
            self.convert_data_types(
                data
            )
        )

        # -----------------------------------------------------
        # Automatic badge.
        # -----------------------------------------------------

        if not data["badge"]:

            data["badge"] = (
                self.make_badge(
                    data["deadline"]
                )
            )

        # -----------------------------------------------------
        # Add to list.
        # -----------------------------------------------------

        self.scholarships.append(
            data
        )

        # -----------------------------------------------------
        # Generate HTML immediately.
        # -----------------------------------------------------

        try:

            output_path = (
                self.generate_html_for_scholarship(
                    data
                )
            )

            html_message = (
                f"HTML page created:\n"
                f"{output_path}"
            )

        except Exception as exc:

            html_message = (
                "Scholarship added, but HTML "
                "generation failed:\n"
                f"{exc}"
            )

        # -----------------------------------------------------
        # Refresh GUI.
        # -----------------------------------------------------

        self.refresh_list()

        self.clear_form(
            self.add_vars
        )

        self.notebook.select(
            self.view_tab
        )

        self.set_status(
            "Scholarship added! "
            "HTML page generated. "
            "Press Ctrl+S to save."
        )

        # -----------------------------------------------------
        # If generation failed, tell user.
        # -----------------------------------------------------

        if "failed" in html_message.lower():

            messagebox.showwarning(
                "HTML Generation Warning",
                html_message,
            )

    # =========================================================
    # Update Scholarship
    # =========================================================

    def update_scholarship(self):

        if self.current_index is None:

            self.set_status(
                "No scholarship selected.",
                error=True,
            )

            messagebox.showwarning(
                "No Selection",
                "No scholarship is currently selected.",
            )

            return

        # -----------------------------------------------------
        # Get form.
        # -----------------------------------------------------

        data = self.get_form_data(
            self.edit_vars
        )

        # -----------------------------------------------------
        # Validate.
        # -----------------------------------------------------

        valid, error = (
            self.validate_form(
                data
            )
        )

        if not valid:

            self.set_status(
                error,
                error=True,
            )

            messagebox.showwarning(
                "Invalid Scholarship",
                error,
            )

            return

        # -----------------------------------------------------
        # Convert types.
        # -----------------------------------------------------

        data = (
            self.convert_data_types(
                data
            )
        )

        # -----------------------------------------------------
        # Automatic badge.
        # -----------------------------------------------------

        if not data["badge"]:

            data["badge"] = (
                self.make_badge(
                    data["deadline"]
                )
            )

        # -----------------------------------------------------
        # Remember old HTML filename.
        # -----------------------------------------------------

        old_scholarship = (
            self.scholarships[
                self.current_index
            ]
        )

        old_filename = (
            self.get_html_filename(
                old_scholarship
            )
        )

        # -----------------------------------------------------
        # Replace data.
        # -----------------------------------------------------

        self.scholarships[
            self.current_index
        ] = data

        # -----------------------------------------------------
        # Generate new HTML.
        # -----------------------------------------------------

        try:

            new_path = (
                self.generate_html_for_scholarship(
                    data
                )
            )

            new_filename = (
                new_path.name
            )

            # ---------------------------------------------
            # If filename changed, delete old page.
            # ---------------------------------------------

            if (
                old_filename
                != new_filename
            ):

                old_path = (
                    self.html_directory
                    / old_filename
                )

                if old_path.exists():

                    old_path.unlink()

            html_status = (
                "HTML page regenerated."
            )

        except Exception as exc:

            html_status = (
                "HTML generation failed: "
                f"{exc}"
            )

        # -----------------------------------------------------
        # Refresh.
        # -----------------------------------------------------

        self.refresh_list()

        self.notebook.select(
            self.view_tab
        )

        self.set_status(
            "Scholarship updated! "
            + html_status
            + " Press Ctrl+S to save."
        )

    # =========================================================
    # Delete Scholarship
    # =========================================================

    def delete_scholarship(self):

        if self.current_index is None:

            self.set_status(
                "No scholarship selected.",
                error=True,
            )

            messagebox.showwarning(
                "No Selection",
                "No scholarship is currently selected.",
            )

            return

        scholarship = (
            self.scholarships[
                self.current_index
            ]
        )

        name = scholarship.get(
            "name",
            "Unnamed",
        )

        # -----------------------------------------------------
        # Confirmation.
        # -----------------------------------------------------

        confirmed = (
            messagebox.askyesno(
                "Delete Scholarship",
                "Are you sure you want to delete:\n\n"
                f"{name}\n\n"
                "The JSON entry and generated HTML "
                "page will be removed when you save.",
            )
        )

        if not confirmed:

            return

        # -----------------------------------------------------
        # Remove generated HTML page.
        # -----------------------------------------------------

        try:

            filename = (
                self.get_html_filename(
                    scholarship
                )
            )

            html_path = (
                self.html_directory
                / filename
            )

            if html_path.exists():

                html_path.unlink()

        except Exception:

            pass

        # -----------------------------------------------------
        # Remove JSON item.
        # -----------------------------------------------------

        self.scholarships.pop(
            self.current_index
        )

        self.current_index = None

        # -----------------------------------------------------
        # Refresh GUI.
        # -----------------------------------------------------

        self.refresh_list()

        self.clear_form(
            self.edit_vars
        )

        self.update_preview()

        self.notebook.select(
            self.view_tab
        )

        self.set_status(
            f"Deleted: {name}. "
            "Press Ctrl+S to save."
        )


# =============================================================
# ENTRY POINT
# =============================================================

if __name__ == "__main__":

    app = ScholarshipEditor()

    app.mainloop()

