import calendar
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stylish Expense Tracker")
        self.root.geometry("860x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6fb")

        self.entries = []
        self.build_ui()

    def build_ui(self):
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)
        main.configure(style="Main.TFrame")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Main.TFrame", background="#fdf4ff")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#ffffff", foreground="#7c3aed", font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", background="#ffffff", foreground="#8b5cf6", font=("Segoe UI", 10))
        style.configure("Label.TLabel", background="#ffffff", foreground="#374151", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), foreground="white", background="#4f46e5")
        style.map("Accent.TButton", background=[("active", "#4338ca"), ("!disabled", "#4f46e5")])
        style.configure("Soft.TButton", font=("Segoe UI", 10, "bold"), foreground="#7c3aed", background="#ede9fe")
        style.map("Soft.TButton", background=[("active", "#ddd6fe"), ("!disabled", "#ede9fe")])

        title_frame = ttk.Frame(main, style="Card.TFrame")
        title_frame.pack(fill="x", pady=(0, 12))
        ttk.Label(title_frame, text="Expense Tracker", style="Title.TLabel").pack(anchor="w", padx=16, pady=(12, 2))
        ttk.Label(title_frame, text="Track your spending in a clean, modern way", style="Subtitle.TLabel").pack(anchor="w", padx=16, pady=(0, 12))

        form_frame = ttk.Frame(main, style="Card.TFrame")
        form_frame.pack(fill="x", pady=(0, 12))
        form_frame.columnconfigure(1, weight=1)

        self.fields = {}
        labels = [
            ("Date", "date"),
            ("Description", "desc"),
            ("Amount", "amount"),
            ("Category", "category"),
        ]

        for index, (label_text, key) in enumerate(labels):
            ttk.Label(form_frame, text=label_text, style="Label.TLabel").grid(row=index, column=0, sticky="w", padx=16, pady=8)
            var = tk.StringVar()
            if key == "date":
                var.set(date.today().strftime("%Y-%m-%d"))
            elif key == "category":
                var.set("General")
            self.fields[key] = var

            if key == "date":
                date_entry = ttk.Entry(form_frame, textvariable=var, width=30)
                date_entry.grid(row=index, column=1, sticky="ew", padx=16, pady=8)
                ttk.Button(form_frame, text="📅 Pick", style="Soft.TButton", command=lambda v=var: self.pick_date(v)).grid(row=index, column=2, padx=(0, 16), pady=8)
            else:
                ttk.Entry(form_frame, textvariable=var, width=30).grid(row=index, column=1, sticky="ew", padx=16, pady=8)

        button_row = ttk.Frame(form_frame)
        button_row.grid(row=4, column=0, columnspan=3, sticky="w", padx=16, pady=(10, 16))
        ttk.Button(button_row, text="💾 Save Entry", style="Accent.TButton", command=self.save_entry).pack(side="left", padx=(0, 8))
        ttk.Button(button_row, text="🧹 Clear Form", style="Soft.TButton", command=self.clear_form).pack(side="left")

        entries_frame = ttk.Frame(main, style="Card.TFrame")
        entries_frame.pack(fill="both", expand=True)
        entries_frame.columnconfigure(0, weight=1)
        entries_frame.rowconfigure(1, weight=1)

        ttk.Label(entries_frame, text="Recent Entries", style="Label.TLabel", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 6))

        self.diary_text = tk.Text(entries_frame, height=16, width=90, wrap="word", bd=0, bg="#f9fafb", fg="#374151")
        self.diary_text.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.diary_text.insert("1.0", "No entries yet.\n")

        bottom_row = ttk.Frame(entries_frame)
        bottom_row.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        ttk.Label(bottom_row, text="Total Spent:", style="Label.TLabel").pack(side="left")
        self.total_var = tk.StringVar(value="$0.00")
        ttk.Label(bottom_row, textvariable=self.total_var, font=("Segoe UI", 11, "bold"), foreground="#2563eb").pack(side="left", padx=(8, 0))

    def pick_date(self, var):
        popup = tk.Toplevel(self.root)
        popup.title("Choose Date")
        popup.geometry("320x330")
        popup.transient(self.root)
        popup.grab_set()
        popup.configure(bg="#fff7ed")

        current_year = date.today().year
        current_month = date.today().month
        selected_date = date.today()

        header = tk.Frame(popup, bg="#fff7ed")
        header.pack(fill="x", padx=12, pady=(12, 8))

        def update_calendar():
            for widget in calendar_frame.winfo_children():
                widget.destroy()

            month_label.config(text=f"{calendar.month_name[current_month]} {current_year}")

            weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
            for col, day_name in enumerate(weekdays):
                tk.Label(calendar_frame, text=day_name, width=4, bg="#fef3c7", fg="#92400e", font=("Segoe UI", 9, "bold")).grid(row=0, column=col, padx=2, pady=2)

            weeks = calendar.monthcalendar(current_year, current_month)
            for row_index, week in enumerate(weeks, start=1):
                for col_index, day in enumerate(week):
                    if day == 0:
                        tk.Label(calendar_frame, text="", width=4, height=2, bg="#fff7ed").grid(row=row_index, column=col_index, padx=2, pady=2)
                    else:
                        day_date = date(current_year, current_month, day)
                        btn = tk.Button(
                            calendar_frame,
                            text=str(day),
                            width=4,
                            height=2,
                            bg="#ffffff" if day_date != selected_date else "#4f46e5",
                            fg="#111827" if day_date != selected_date else "white",
                            relief="raised",
                            bd=1,
                            command=lambda d=day_date: select_day(d),
                        )
                        btn.grid(row=row_index, column=col_index, padx=2, pady=2)

        def select_day(day_value):
            nonlocal selected_date
            selected_date = day_value
            var.set(selected_date.strftime("%Y-%m-%d"))
            popup.destroy()

        def change_month(step):
            nonlocal current_month, current_year
            current_month += step
            if current_month == 13:
                current_month = 1
                current_year += 1
            elif current_month == 0:
                current_month = 12
                current_year -= 1
            update_calendar()

        tk.Button(header, text="◀", command=lambda: change_month(-1), bg="#ede9fe", fg="#6d28d9", relief="flat").pack(side="left")
        month_label = tk.Label(header, text="", bg="#fff7ed", fg="#7c3aed", font=("Segoe UI", 11, "bold"))
        month_label.pack(side="left", expand=True)
        tk.Button(header, text="▶", command=lambda: change_month(1), bg="#ede9fe", fg="#6d28d9", relief="flat").pack(side ="left")

        calendar_frame = tk.Frame(popup, bg="#fff7ed")
        calendar_frame.pack(padx=10, pady=8)

        update_calendar()

        tk.Button(popup, text="Select Date", bg="#4f46e5", fg="white", command=lambda: select_day(selected_date), relief="flat").pack(pady=(8, 12))

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

    def display_entries(self):
        self.diary_text.delete("1.0", tk.END)
        total = sum(item["amount"] for item in self.entries)
        self.total_var.set(f"${total:,.2f}")

        if not self.entries:
            self.diary_text.insert("1.0", "No entries yet.\n")
            return

        for item in self.entries:
            self.diary_text.insert(tk.END, f"📅 {item['date']}\n")
            self.diary_text.insert(tk.END, f"🏷️ {item['category']}\n")
            self.diary_text.insert(tk.END, f"🛍️ {item['description']}\n")
            self.diary_text.insert(tk.END, f"💵 ${item['amount']:.2f}\n")
            self.diary_text.insert(tk.END, "-" * 40 + "\n")

    def clear_form(self):
        self.fields["date"].set(date.today().strftime("%Y-%m-%d"))
        self.fields["desc"].set("")
        self.fields["amount"].set("")
        self.fields["category"].set("General")


if __name__ == "__main__":
    root = tk.Tk()
    ExpenseTrackerApp(root)
    root.mainloop()


