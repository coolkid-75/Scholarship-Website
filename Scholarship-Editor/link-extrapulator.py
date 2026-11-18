import json
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path


JSON_FILE = Path(
    "/home/coolkid75/Scholarship-Website/public/data/scholarships.json"
)


class ScholarshipExtractor:

    def __init__(self, root):
        self.root = root
        self.root.title("Scholarship Name & Link Extractor")
        self.root.geometry("1050x650")
        self.root.minsize(800, 500)

        self.scholarships = []
        self.filtered_scholarships = []

        self.build_gui()
        self.load_json()

    def build_gui(self):

        header = ttk.Label(
            self.root,
            text="Scholarship Name & Application Link Extractor",
            font=("Arial", 18, "bold")
        )
        header.pack(pady=15)

        # Search
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace_add(
            "write",
            self.search_scholarships
        )

        ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=50
        ).pack(side="left", padx=10)

        # Main table
        table_frame = ttk.Frame(self.root)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=("name", "link"),
            show="headings"
        )

        self.tree.heading("name", text="Scholarship Name")
        self.tree.heading("link", text="Application Link")

        self.tree.column("name", width=350, anchor="w")
        self.tree.column("link", width=600, anchor="w")

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.display_selected
        )

        # Copyable display
        display_frame = ttk.LabelFrame(
            self.root,
            text="Scholarship Data"
        )
        display_frame.pack(fill="x", padx=15, pady=5)

        self.text_display = tk.Text(
            display_frame,
            height=5,
            wrap="word",
            font=("Consolas", 10)
        )

        self.text_display.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # Only three action buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=15, pady=10)

        ttk.Button(
            button_frame,
            text="Copy All",
            command=self.copy_all
        ).pack(side="left", padx=5, expand=True, fill="x")

        ttk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_csv
        ).pack(side="left", padx=5, expand=True, fill="x")

        ttk.Button(
            button_frame,
            text="Refresh JSON",
            command=self.load_json
        ).pack(side="left", padx=5, expand=True, fill="x")

        # Status bar
        self.status = ttk.Label(
            self.root,
            text="Ready",
            relief="sunken",
            anchor="w"
        )
        self.status.pack(fill="x", side="bottom")

    def load_json(self):

        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError(
                    "JSON must contain a list of scholarships."
                )

            self.scholarships = []

            for item in data:

                if not isinstance(item, dict):
                    continue

                self.scholarships.append({
                    "name": item.get("name", ""),
                    "applicationUrl": item.get(
                        "applicationUrl", ""
                    )
                })

            self.search_var.set("")
            self.filtered_scholarships = self.scholarships.copy()

            self.populate_table()

            self.status.config(
                text=f"Loaded {len(self.scholarships)} scholarships."
            )

        except FileNotFoundError:
            messagebox.showerror(
                "File Not Found",
                f"Could not find:\n{JSON_FILE}"
            )

        except json.JSONDecodeError as error:
            messagebox.showerror(
                "Invalid JSON",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error)
            )

    def populate_table(self):

        self.tree.delete(*self.tree.get_children())

        for index, scholarship in enumerate(
            self.filtered_scholarships
        ):

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    scholarship["name"],
                    scholarship["applicationUrl"]
                )
            )

        self.status.config(
            text=f"Showing {len(self.filtered_scholarships)} "
                 f"of {len(self.scholarships)} scholarships."
        )

    def search_scholarships(self, *args):

        query = self.search_var.get().lower().strip()

        self.filtered_scholarships = [
            scholarship
            for scholarship in self.scholarships
            if query in scholarship["name"].lower()
            or query in scholarship["applicationUrl"].lower()
        ]

        self.populate_table()

    def display_selected(self, event=None):

        selected = self.tree.selection()

        self.text_display.delete("1.0", tk.END)

        for item_id in selected:

            scholarship = self.filtered_scholarships[
                int(item_id)
            ]

            self.text_display.insert(
                tk.END,
                f"Name: {scholarship['name']}\n"
                f"Link: {scholarship['applicationUrl']}\n\n"
            )

    def copy_all(self):

        if not self.scholarships:
            messagebox.showwarning(
                "No Data",
                "There are no scholarships to copy."
            )
            return

        lines = []

        for scholarship in self.scholarships:

            lines.append(
                f"{scholarship['name']}\t"
                f"{scholarship['applicationUrl']}"
            )

        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(lines))
        self.root.update()

        self.status.config(
            text=f"Copied {len(self.scholarships)} scholarships!"
        )

    def export_csv(self):

        if not self.scholarships:
            messagebox.showwarning(
                "No Data",
                "There are no scholarships to export."
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="scholarship_links.csv"
        )

        if not filename:
            return

        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=["name", "applicationUrl"]
                )

                writer.writeheader()
                writer.writerows(self.scholarships)

            messagebox.showinfo(
                "Export Successful",
                f"Exported {len(self.scholarships)} scholarships!\n\n"
                f"Saved to:\n{filename}"
            )

            self.status.config(
                text="CSV export successful!"
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )


if __name__ == "__main__":

    root = tk.Tk()
    app = ScholarshipExtractor(root)
    root.mainloop()

