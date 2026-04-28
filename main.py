import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.file_path = 'expenses.json'
        self.expenses = self.load_data()

        # Настройка интерфейса
        self.setup_ui()
        self.update_table(self.expenses)

    def setup_ui(self):
        # Поля ввода
        frame_input = tk.LabelFrame(self.root, text="Добавить расход")
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_amount = tk.Entry(frame_input)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_category = ttk.Combobox(frame_input, values=["Еда", "Транспорт", "Развлечения", "Другое"])
        self.combo_category.grid(row=1, column=1, padx=5, pady=5)
        self.combo_category.set("Еда")

        tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=2, column=1, padx=5, pady=5)

        btn_add = tk.Button(frame_input, text="Добавить расход", command=self.add_expense)
        btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # Блок фильтрации
        frame_filter = tk.LabelFrame(self.root, text="Фильтрация и Итоги")
        frame_filter.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filter, text="Категория:").grid(row=0, column=0)
        self.filter_cat = ttk.Combobox(frame_filter, values=["Все", "Еда", "Транспорт", "Развлечения", "Другое"])
        self.filter_cat.set("Все")
        self.filter_cat.grid(row=0, column=1)

        tk.Label(frame_filter, text="Дата:").grid(row=1, column=0)
        self.filter_date = tk.Entry(frame_filter)
        self.filter_date.grid(row=1, column=1)

        btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter)
        btn_filter.grid(row=2, column=0, columnspan=2, pady=5)

        self.label_total = tk.Label(frame_filter, text="Итого за период: 0", font=('Arial', 10, 'bold'))
        self.label_total.grid(row=3, column=0, columnspan=2)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Сумма", "Категория", "Дата"), show='headings')
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

    def add_expense(self):
        amount = self.entry_amount.get()
        category = self.combo_category.get()
        date_str = self.entry_date.get()

        # Валидация
        try:
            amount_val = float(amount)
            if amount_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
            return

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return

        new_item = {"amount": amount_val, "category": category, "date": date_str}
        self.expenses.append(new_item)
        self.save_data()
        self.update_table(self.expenses)
        
        # Очистка поля суммы после добавления
        self.entry_amount.delete(0, tk.END)

    def apply_filter(self):
        cat = self.filter_cat.get()
        date = self.filter_date.get()
        
        filtered = self.expenses
        if cat != "Все":
            filtered = [x for x in filtered if x['category'] == cat]
        if date:
            filtered = [x for x in filtered if date in x['date']]
        
        self.update_table(filtered)

    def update_table(self, data_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total = 0
        for item in data_list:
            self.tree.insert("", "end", values=(item['amount'], item['category'], item['date']))
            total += item['amount']
        
        self.label_total.config(text=f"Итого за период: {total:.2f}")

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
