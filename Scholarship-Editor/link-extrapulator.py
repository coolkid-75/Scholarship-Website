import json
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from urllib.parse import urlparse


JSON_FILE = Path(
    "/home/coolkid75/Scholarship-Website/public/data/scholarships.json"
)


class ScholarshipExtractor:

    def __init__(self, root):
        self.root = root
        self.root.title("Root Domain Extractor")
        self.root.geometry("750x600")
        self.root.minsize(600, 400)

        self.domains = []
        self.filtered_domains = []

        self.build_gui()
        self.load_json()

    def build_gui(self):

        header = ttk.Label(
            self.root,
            text="Scholarship Root Domain Extractor",
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
            self.search_domains
        )

        ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=50
        ).pack(side="left", padx=10)

        # Domain table
        table_frame = ttk.Frame(self.root)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=("domain",),
            show="headings"
        )

        self.tree.heading("domain", text="Root Domain")
        self.tree.column("domain", width=600, anchor="w")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons
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

    def extract_root_domain(self, url):

        if not url:
            return None

        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            hostname = urlparse(url).hostname

            if not hostname:
                return None

            hostname = hostname.lower().rstrip(".")

            if hostname.startswith("www."):
                hostname = hostname[4:]

            # Return the registered root domain.
            # Handles common multi-part suffixes such as .co.uk.
            import tldextract

            extracted = tldextract.extract(hostname)

            if extracted.domain and extracted.suffix:
                return f"{extracted.domain}.{extracted.suffix}"

            return hostname

        except Exception:
            return None

    def load_json(self):

        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError(
                    "JSON must contain a list of scholarships."
                )

            unique_domains = set()

            for item in data:

                if not isinstance(item, dict):
                    continue

                domain = self.extract_root_domain(
                    item.get("applicationUrl", "")
                )

                if domain:
                    unique_domains.add(domain)

            self.domains = sorted(unique_domains)

            self.search_var.set("")
            self.filtered_domains = self.domains.copy()

            self.populate_table()

            self.status.config(
                text=f"Found {len(self.domains)} unique root domains."
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

        for domain in self.filtered_domains:
            self.tree.insert(
                "",
                "end",
                values=(domain,)
            )

        self.status.config(
            text=f"Showing {len(self.filtered_domains)} "
                 f"of {len(self.domains)} root domains."
        )

    def search_domains(self, *args):

        query = self.search_var.get().lower().strip()

        self.filtered_domains = [
            domain
            for domain in self.domains
            if query in domain.lower()
        ]

        self.populate_table()

    def copy_all(self):

        if not self.domains:
            messagebox.showwarning(
                "No Data",
                "There are no domains to copy."
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(self.domains))
        self.root.update()

        self.status.config(
            text=f"Copied {len(self.domains)} root domains!"
        )

    def export_csv(self):

        if not self.domains:
            messagebox.showwarning(
                "No Data",
                "There are no domains to export."
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="root_domains.csv"
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

                writer = csv.writer(file)
                writer.writerow(["Root Domain"])

                for domain in self.domains:
                    writer.writerow([domain])

            messagebox.showinfo(
                "Export Successful",
                f"Exported {len(self.domains)} root domains!\n\n"
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
