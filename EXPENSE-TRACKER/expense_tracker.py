import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date

try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root  # Main window
        self.graph_frame = None  # Frame for the graph
        self.figure = None  # Matplotlib figure
        self.ax = None  # Matplotlib axes
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")
        self.root.resizable(True,True)

        self.entries = []  # Stores all saved expense entries
        self.build_ui()

    def build_ui(self):
        main = ttk.Frame(self.root, padding=12)  # Main layout container
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Expense Tracker", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 10)
        )

        self.fields = {}  # Holds the input variables
        labels = [
            ("Date:", "(YYYY-MM-DD)", "date"),
            ("Description:", "(what did you buy?)", "desc"),
            ("Amount:", "(e.g. 15.50)", "amount"),
            ("Category:", "(Food, Travel, Bills)", "category"),
        ]

        for i, (label_text, hint, key) in enumerate(labels, start=1):
            ttk.Label(main, text=label_text).grid(row=i, column=0, sticky="w")
            var = tk.StringVar()
            if key == "date":
                var.set(date.today().strftime("%Y-%m-%d"))
            elif key == "category":
                var.set("General")
            self.fields[key] = var

            if key == "date" and DateEntry is not None:
                widget = DateEntry(main, textvariable=var, date_pattern="yyyy-mm-dd", width=28)
            else:
                widget = ttk.Entry(main, textvariable=var, width=30)
            widget.grid(row=i, column=1, sticky="ew", pady=3)
            ttk.Label(main, text=hint, foreground="gray").grid(row=i, column=2, sticky="w", padx=(6, 0))

        button_row = ttk.Frame(main)  # Buttons section
        button_row.grid(row=5, column=0, columnspan=3, sticky="w", pady=10)
        ttk.Button(button_row, text="Save Entry", command=self.save_entry).pack(side="left", padx=(0, 8))
        ttk.Button(button_row, text="Clear Form", command=self.clear_form).pack(side="left")

        ttk.Label(main, text="Diary Entries").grid(row=6, column=0, columnspan=3, sticky="w", pady=(10, 5))

        self.diary_text = tk.Text(main, height=16, width=80, wrap="word")  # Diary display area
        self.diary_text.grid(row=7, column=0, columnspan=3, sticky="nsew")
        self.diary_text.insert("1.0", "No entries yet.\n")

        ttk.Label(main, text="Total Spent:").grid(row=8, column=0, sticky="w", pady=(8, 0))
        self.total_var = tk.StringVar(value="$0.00")
        ttk.Label(main, textvariable=self.total_var, font=("Segoe UI", 11, "bold")).grid(row=8, column=1, sticky="w", pady=(8, 0))

        ttk.Button(main, text="Open Graph Window", command=self.open_graph_window).grid(
            row=9, column=0, columnspan=3, sticky="w", pady=(10, 0)
        )

        self.figure, self.ax = plt.subplots(figsize=(9, 4), dpi=100)
        self.figure.tight_layout()
        self.canvas = None
        self.graph_window = None

        main.columnconfigure(1, weight=1)
        main.rowconfigure(7, weight=1)

    def save_entry(self):
        date_value = self.fields["date"].get().strip()
        desc = self.fields["desc"].get().strip()
        amount_text = self.fields["amount"].get().strip()
        category = self.fields["category"].get().strip() or "General"

        if not date_value or not desc or not amount_text:
            messagebox.showwarning("Missing Fields", "Please fill in the date, description, and amount.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number for the amount.")
            return

        self.entries.append({"date": date_value, "description": desc, "amount": amount, "category": category})
        self.display_entries()
        self.clear_form()

    def open_graph_window(self):
        if self.graph_window is not None and tk.Toplevel.winfo_exists(self.graph_window):
            self.graph_window.lift()
            return

        self.graph_window = tk.Toplevel(self.root)
        self.graph_window.title("Expense Graph")
        self.graph_window.geometry("900x500")

        graph_frame = ttk.Frame(self.graph_window, padding=8)
        graph_frame.pack(fill="both", expand=True)

        canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas = canvas
        self.update_graph()

    def display_entries(self):
        self.diary_text.delete("1.0", tk.END)
        total = sum(item["amount"] for item in self.entries)
        self.total_var.set(f"${total:,.2f}")
        self.update_graph()

        if not self.entries:
            self.diary_text.insert("1.0", "No entries yet.\n")
            return

        for item in self.entries:
            self.diary_text.insert(tk.END, f"Date: {item['date']}\n")
            self.diary_text.insert(tk.END, f"Category: {item['category']}\n")
            self.diary_text.insert(tk.END, f"Description: {item['description']}\n")
            self.diary_text.insert(tk.END, f"Amount: ${item['amount']:.2f}\n")
            self.diary_text.insert(tk.END, "-" * 40 + "\n")

    def update_graph(self):
        self.ax.clear()
        if not self.entries:
            self.ax.set_title("Spending Curve")
            self.ax.set_xlabel("Entries")
            self.ax.set_ylabel("Total Spent ($)")
            if self.canvas is not None:
                self.canvas.draw_idle()
            return

        labels = [item["date"] for item in self.entries]
        cumulative = []
        running_total = 0.0
        for item in self.entries:
            running_total += item["amount"]
            cumulative.append(running_total)

        self.ax.plot(labels, cumulative, marker="o", linewidth=2, color="#007acc")
        self.ax.set_title("Cumulative Spending")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Total Spent ($)")
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.figure.autofmt_xdate(rotation=30)
        if self.canvas is not None:
            self.canvas.draw_idle()

    def clear_form(self):
        self.fields["date"].set(date.today().strftime("%Y-%m-%d"))
        self.fields["desc"].set("")
        self.fields["amount"].set("")
        self.fields["category"].set("General")


if __name__ == "__main__":
    root = tk.Tk()
    ExpenseTrackerApp(root)
    root.mainloop()

