import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import matplotlib.pyplot as plt

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("1300x650")
        self.expenses = []
        self.categories = [
            "Thức ăn",
            "Phương tiện đi lại",
            "Tiện ích",
            "Giải trí",
            "Khác",
        ]
        self.category_var = tk.StringVar(self)
        self.category_var.set(self.categories[0])
        self.create_widgets()
###
    def create_widgets(self):
        self.label = tk.Label(
            self, text="Expense Tracker", font=("Helvetica", 20, "bold")
        )
        self.label.pack(pady=10)
        self.frame_input = tk.Frame(self)
        self.frame_input.pack(pady=10)
        self.expense_label = tk.Label(
            self.frame_input, text="Số tiền:", font=("Helvetica", 12)
        )
        self.expense_label.grid(row=0, column=0, padx=5)
        self.expense_entry = tk.Entry(
            self.frame_input, font=("Helvetica", 12), width=15
        )
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(pady=10)
        self.search_label = tk.Label(self.search_frame, text="Tìm kiếm:", font=("Helvetica", 12))
        self.search_label.grid(row=0, column=0, padx=5)
        self.search_entry = tk.Entry(self.search_frame, font=("Helvetica", 12), width=20)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.item_label = tk.Label(
            self.frame_input, text="Mô tả nội dung:", font=("Helvetica", 12)
        )
        self.item_label.grid(row=0, column=2, padx=5)
        self.item_entry = tk.Entry(self.frame_input, font=("Helvetica", 12), width=20)
        self.item_entry.grid(row=0, column=3, padx=5)
        self.category_label = tk.Label(
            self.frame_input, text="Loại:", font=("Helvetica", 12)
        )
        self.category_label.grid(row=0, column=4, padx=5)
        self.category_dropdown = ttk.Combobox(
            self.frame_input,
            textvariable=self.category_var,
            values=self.categories,
            font=("Helvetica", 12),
            width=15,
        )
        self.category_dropdown.grid(row=0, column=5, padx=5)
        self.date_label = tk.Label(
            self.frame_input, text="Date (DD-MM-YYYY):", font=("Helvetica", 12)
        )
        self.date_label.grid(row=0, column=6, padx=5)
        self.date_entry = tk.Entry(self.frame_input, font=("Helvetica", 12), width=15)
        self.date_entry.grid(row=0, column=7, padx=5)
        ###
        self.search_button = tk.Button(
            self.search_frame, text="Tìm", command=self.search_expenses
        )
        self.search_button.grid(row=0, column=2, padx=5)    
        self.expense_entry.grid(row=0, column=1, padx=5)
        self.show_all_button = tk.Button(
            self, text="Xem tất cả", command=lambda: self.refresh_list(show_all=True)
        )
        self.show_all_button.pack(pady=5)
        self.add_button = tk.Button(self, text="Thêm chi phí", command=self.add_expense)
        self.add_button.pack(pady=5)
        self.frame_list = tk.Frame(self)
        self.frame_list.pack(pady=10)
        self.scrollbar = tk.Scrollbar(self.frame_list)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expense_listbox = tk.Listbox(
            self.frame_list,
            font=("Helvetica", 12),
            width=70,
            yscrollcommand=self.scrollbar.set,
        )
        self.expense_listbox.pack(pady=5)
        self.scrollbar.config(command=self.expense_listbox.yview)
        self.edit_button = tk.Button(
            self, text="Chỉnh sửa chi phí", command=self.edit_expense
        )
        self.edit_button.pack(pady=5)
        self.delete_button = tk.Button(
            self, text="Xóa chi phí", command=self.delete_expense
        )
        self.delete_button.pack(pady=5)
        self.save_button = tk.Button(
            self, text="Lưu chi phí", command=self.save_expenses
        )
        self.save_button.pack(pady=5)
        self.total_label = tk.Label(
            self, text="Tổng chi phí:", font=("Helvetica", 12)
        )
        self.total_label.pack(pady=5)
        self.show_chart_button = tk.Button(
            self, text="Hiển thị sơ đồ chi phí", command=self.show_expenses_chart
        )
        self.show_chart_button.pack(pady=5)
        self.update_total_label()
        ###
    def add_expense(self):
        expense = self.expense_entry.get()
        item = self.item_entry.get()
        category = self.category_var.get()
        date = self.date_entry.get()
        if expense and date:
            self.expenses.append((expense, item, category, date))
            self.expense_listbox.insert(
                tk.END, f"{expense} - {item} - {category} ({date})"
            )
            self.expense_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Chú ý", "Chi phí và ngày không được để trống.")
        self.update_total_label()
    def edit_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_expense = self.expenses[selected_index]
            new_expense = simpledialog.askstring(
                "Chỉnh sửa chi phí", "Nhập chi phí mới:", initialvalue=selected_expense[0]
            )
            if new_expense:
                self.expenses[selected_index] = (
                    new_expense,
                    selected_expense[1],
                    selected_expense[2],
                    selected_expense[3],
                )
                self.refresh_list()
                self.update_total_label()
    def delete_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            del self.expenses[selected_index]
            self.expense_listbox.delete(selected_index)
            self.update_total_label()
    def refresh_list(self,show_all=True):
        self.expense_listbox.delete(0, tk.END)
        if show_all:
            for expense, item, category, date in self.expenses:
                self.expense_listbox.insert(
                    tk.END, f"{expense} - {item} - {category} ({date})"
            )
    def update_total_label(self):
        total_expenses = sum(float(expense[0]) for expense in self.expenses)
        self.total_label.config(text=f"Tổng chi phí:{total_expenses:.3f} VND")

    def save_expenses(self):
        with open("expenses.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            column_headers = ["Số tiền", "Mô tả nội dung", "Loại", "Date"]
            writer.writerow(column_headers)
            for expense in self.expenses:
                writer.writerow(expense)
    def search_expenses(self):
        query = self.search_entry.get().lower()
        if not query:
            messagebox.showwarning("Chú ý", "Hãy nhập từ khóa để tìm kiếm.")
            return

        filtered_expenses = [
            f"{expense} - {item} - {category} ({date})"
            for expense, item, category, date in self.expenses
            if query in expense.lower()
            or query in item.lower()
            or query in category.lower()
            or query in date.lower()
        ]
        if not filtered_expenses:
            messagebox.showinfo("Kết quả", "Không tìm thấy chi phí nào phù hợp.")
            return
        self.expense_listbox.delete(0, tk.END)
        for expense in filtered_expenses:
            self.expense_listbox.insert(tk.END, expense)
    def show_expenses_chart(self):
        category_totals = {}
        for expense, _, category, _ in self.expenses:
            try:
                amount = float(expense)
            except ValueError:
                continue
            category_totals[category] = category_totals.get(category, 0) + amount
        categories = list(category_totals.keys())
        expenses = list(category_totals.values())
        plt.figure(figsize=(8, 6))
        plt.pie(
            expenses, labels=categories, autopct="%1.1f%%", startangle=140, shadow=True
        )
        plt.axis("equal")
        plt.title(f"Sơ đồ chi phí ngày hôm nay")
        plt.show()
if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()