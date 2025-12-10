import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os


class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый учет")
        self.root.geometry("800x600")

        self.transactions = []
        self.load_data()

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Верхняя панель - баланс
        balance_frame = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        balance_frame.pack(fill=tk.X)

        tk.Label(balance_frame, text="Текущий баланс:",
                 font=("Arial", 14), bg="#2c3e50", fg="white").pack()
        self.balance_label = tk.Label(balance_frame, text="0 ₽",
                                      font=("Arial", 24, "bold"),
                                      bg="#2c3e50", fg="#2ecc71")
        self.balance_label.pack()

        # Панель добавления транзакции
        input_frame = tk.LabelFrame(self.root, text="Добавить операцию",
                                    padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Тип операции
        tk.Label(input_frame, text="Тип:").grid(row=0, column=0, sticky="w")
        self.type_var = tk.StringVar(value="Расход")
        type_frame = tk.Frame(input_frame)
        type_frame.grid(row=0, column=1, sticky="w", pady=5)
        tk.Radiobutton(type_frame, text="Доход", variable=self.type_var,
                       value="Доход", command=self.update_categories).pack(side=tk.LEFT)
        tk.Radiobutton(type_frame, text="Расход", variable=self.type_var,
                       value="Расход", command=self.update_categories).pack(side=tk.LEFT)

        # Сумма
        tk.Label(input_frame, text="Сумма:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(input_frame, width=20)
        self.amount_entry.grid(row=1, column=1, sticky="w", pady=5)

        # Категория
        tk.Label(input_frame, text="Категория:").grid(row=2, column=0, sticky="w")
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var,
                                           width=18, state="readonly")
        self.category_combo.grid(row=2, column=1, sticky="w", pady=5)
        self.update_categories()

        # Описание
        tk.Label(input_frame, text="Описание:").grid(row=3, column=0, sticky="w")
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=3, column=1, columnspan=2, sticky="w", pady=5)

        # Кнопка добавления
        tk.Button(input_frame, text="Добавить", command=self.add_transaction,
                  bg="#3498db", fg="white", padx=20, pady=5).grid(row=4, column=1, pady=10)

        # Панель фильтров
        filter_frame = tk.Frame(self.root, padx=10)
        filter_frame.pack(fill=tk.X, padx=10)

        tk.Label(filter_frame, text="Фильтр:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="Все")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                    width=15, state="readonly")
        filter_combo['values'] = ("Все", "Доходы", "Расходы")
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.update_display())

        tk.Button(filter_frame, text="Очистить историю",
                  command=self.clear_history, bg="#e74c3c",
                  fg="white").pack(side=tk.RIGHT)

        # Таблица транзакций
        list_frame = tk.LabelFrame(self.root, text="История операций", padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview
        columns = ("Дата", "Тип", "Категория", "Сумма", "Описание")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings",
                                 yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Настройка колонок
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Описание", text="Описание")

        self.tree.column("Дата", width=150)
        self.tree.column("Тип", width=80)
        self.tree.column("Категория", width=120)
        self.tree.column("Сумма", width=100)
        self.tree.column("Описание", width=250)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Контекстное меню для удаления
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Удалить", command=self.delete_transaction)

    def update_categories(self):
        if self.type_var.get() == "Доход":
            categories = ["Зарплата", "Фриланс", "Подарок", "Инвестиции", "Другое"]
        else:
            categories = ["Продукты", "Транспорт", "Развлечения", "Здоровье",
                          "Образование", "Коммунальные", "Одежда", "Другое"]

        self.category_combo['values'] = categories
        if categories:
            self.category_var.set(categories[0])

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму")
            return

        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": self.type_var.get(),
            "category": self.category_var.get(),
            "amount": amount,
            "description": self.desc_entry.get()
        }

        self.transactions.append(transaction)
        self.save_data()
        self.update_display()

        # Очистка полей
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Операция добавлена!")

    def update_display(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Фильтрация транзакций
        filter_type = self.filter_var.get()
        filtered = self.transactions

        if filter_type == "Доходы":
            filtered = [t for t in self.transactions if t["type"] == "Доход"]
        elif filter_type == "Расходы":
            filtered = [t for t in self.transactions if t["type"] == "Расход"]

        # Добавление в таблицу (в обратном порядке - новые сверху)
        for transaction in reversed(filtered):
            amount_str = f"{transaction['amount']:.2f} ₽"
            if transaction['type'] == "Доход":
                tag = "income"
            else:
                tag = "expense"

            self.tree.insert("", 0, values=(
                transaction["date"],
                transaction["type"],
                transaction["category"],
                amount_str,
                transaction["description"]
            ), tags=(tag,))

        # Цвета для разных типов
        self.tree.tag_configure("income", foreground="#2ecc71")
        self.tree.tag_configure("expense", foreground="#e74c3c")

        # Обновление баланса
        balance = sum(t["amount"] if t["type"] == "Доход" else -t["amount"]
                      for t in self.transactions)
        self.balance_label.config(text=f"{balance:.2f} ₽")

        if balance >= 0:
            self.balance_label.config(fg="#2ecc71")
        else:
            self.balance_label.config(fg="#e74c3c")

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранную операцию?"):
            item = selected[0]
            values = self.tree.item(item)['values']

            # Находим и удаляем транзакцию
            for i, t in enumerate(self.transactions):
                if (t["date"] == values[0] and
                        t["type"] == values[1] and
                        t["category"] == values[2]):
                    self.transactions.pop(i)
                    break

            self.save_data()
            self.update_display()

    def clear_history(self):
        if messagebox.askyesno("Подтверждение",
                               "Удалить всю историю операций?"):
            self.transactions = []
            self.save_data()
            self.update_display()

    def save_data(self):
        with open("finance_data.json", "w", encoding="utf-8") as f:
            json.dump(self.transactions, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists("finance_data.json"):
            try:
                with open("finance_data.json", "r", encoding="utf-8") as f:
                    self.transactions = json.load(f)
            except:
                self.transactions = []


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()