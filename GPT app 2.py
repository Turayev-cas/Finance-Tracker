import tkinter as tk
from tkinter import messagebox
import json

# --- КОНСТАНТЫ И ПЕРЕМЕННЫЕ ---
DATA_FILE = "data.json"
balance = 0
history = []


# --- ФУНКЦИИ РАБОТЫ С ДАННЫМИ ---
def save_data():
    data = {
        "balance": balance,
        "history": history,
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные:\n{e}")


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data.get("balance", 0), data.get("history", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, []


# --- ЛОГИКА ---
def extract_number(text_part):
    """Пытается достать число из куска текста (например, '100$')"""
    clean_part = text_part.replace('$', '').replace('+', '')
    # Убираем минус только если он не в начале (чтобы понять, отрицательное ли число, хотя у нас логика другая)
    if clean_part.replace('.', '', 1).isdigit():
        return float(clean_part)
    return None


def update_ui():
    """Обновляет баланс и текстовое поле истории"""
    balance_label.config(text=f"Баланс {balance}$")

    global_history_area.config(state=tk.NORMAL)
    global_history_area.delete(1.0, tk.END)
    history_text = "\n".join(history)
    global_history_area.insert(tk.END, history_text)
    global_history_area.config(state=tk.DISABLED)


def add_transaction(is_income):
    global balance
    try:
        money = float(money_entry.get())
        if money <= 0:
            messagebox.showwarning("Внимание", "Сумма должна быть больше нуля")
            return

        if not is_income and money > balance:
            messagebox.showerror("Ошибка", f"Недостаточно средств!\nБаланс: {balance}$")
            return

        if is_income:
            balance += money
            history.append(f"Доход +{money}$")
        else:
            balance -= money
            history.append(f"Расход -{money}$")  # Убрал пробел перед минусом для красоты

        save_data()
        update_ui()
        money_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число (например: 150 или 150.50)")


def toggle_history_panel():
    if show_history_var.get():
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, expand=True)
        update_ui()
    else:
        right_frame.pack_forget()


def toggle_edit():
    current_state = global_history_area.cget("state")
    if current_state == tk.DISABLED:
        global_history_area.config(state=tk.NORMAL)
        global_history_area.config(bg="#e8f0fe")  # Чуть подкрасим фон, чтобы было видно, что можно писать
        edit_btn.config(text="Отменить ред.")
    else:
        global_history_area.config(state=tk.DISABLED)
        global_history_area.config(bg="white")
        edit_btn.config(text="Редактировать")
        update_ui()  # Возвращаем старый текст, если отменили


def save_edited_history():
    global balance, history

    # Спрашиваем подтверждение, так как это опасная операция
    if not messagebox.askyesno("Подтверждение", "Вы уверены? Баланс будет пересчитан на основе текста."):
        return

    full_text = global_history_area.get(1.0, tk.END).strip()
    if not full_text:
        new_lines = []
    else:
        new_lines = full_text.split("\n")

    temp_balance = 0
    temp_history = []

    error_lines = []

    for line in new_lines:
        line = line.strip()
        if not line: continue

        found_amount = False
        parts = line.split(' ')

        # Ищем число в строке
        amount = 0
        for part in parts:
            val = extract_number(part)
            if val is not None:
                amount = val
                found_amount = True
                break

        if line.startswith("Доход") and found_amount:
            temp_balance += amount
            temp_history.append(line)
        elif line.startswith("Расход") and found_amount:
            temp_balance -= amount
            temp_history.append(line)
        else:
            # Если строка не понятна, просто сохраняем её, но на баланс она не влияет
            # Либо можно помечать как ошибку
            temp_history.append(line)
            # error_lines.append(line) # Раскомментируй, если хочешь видеть ошибки

    # Применяем изменения
    balance = temp_balance
    history = temp_history

    save_data()

    # Выключаем режим редактирования
    global_history_area.config(state=tk.DISABLED, bg="white")
    edit_btn.config(text="Редактировать")

    update_ui()
    messagebox.showinfo("Успешно", "История обновлена и баланс пересчитан!")


# --- ЗАГРУЗКА ---
balance, history = load_data()

# --- ИНТЕРФЕЙС ---
window = tk.Tk()
window.title("Мои Финансы")
window.geometry("900x600")  # Лучше задать конкретный размер, чем zoomed (не везде работает)

# Стили
font_large = ("Arial", 16)
font_btn = ("Arial", 11, "bold")

# Верхняя панель
top_frame = tk.Frame(window)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

balance_label = tk.Label(top_frame, text=f"Баланс {balance}$", font=("Arial", 24, "bold"), fg="#333")
balance_label.pack(pady=10)

show_history_var = tk.BooleanVar(value=False)
history_checkbox = tk.Checkbutton(top_frame, text="Показать историю ➜",
                                  variable=show_history_var, command=toggle_history_panel,
                                  font=("Arial", 10))
history_checkbox.pack(side=tk.RIGHT)

# Основной контейнер
main_container = tk.Frame(window)
main_container.pack(fill=tk.BOTH, expand=True)

# Левая часть (Ввод)
left_frame = tk.Frame(main_container)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

tk.Label(left_frame, text="Сумма операции:", font=("Arial", 12)).pack(anchor="w", pady=(20, 0))
money_entry = tk.Entry(left_frame, font=("Arial", 24))
money_entry.pack(pady=5, fill='x')

btn_frame = tk.Frame(left_frame)
btn_frame.pack(pady=20, fill='x')

tk.Button(btn_frame, text="➕ Доход", command=lambda: add_transaction(True),
          bg="#4CAF50", fg="white", font=font_btn, height=2).pack(side=tk.LEFT, fill='x', expand=True, padx=5)

tk.Button(btn_frame, text="➖ Расход", command=lambda: add_transaction(False),
          bg="#F44336", fg="white", font=font_btn, height=2).pack(side=tk.RIGHT, fill='x', expand=True, padx=5)

# Правая часть (История) - скрыта по умолчанию
right_frame = tk.Frame(main_container, bg="#f5f5f5", width=350)
# right_frame не пакуем сразу, это делает чекбокс

tk.Label(right_frame, text="История операций", bg="#f5f5f5", font=("Arial", 12, "bold")).pack(pady=5)

text_frame = tk.Frame(right_frame)
text_frame.pack(fill=tk.BOTH, expand=True, padx=10)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

global_history_area = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Consolas", 10),
                              state=tk.DISABLED)
global_history_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=global_history_area.yview)

edit_save_frame = tk.Frame(right_frame, bg="#f5f5f5")
edit_save_frame.pack(fill='x', pady=10, padx=10)

edit_btn = tk.Button(edit_save_frame, text="Редактировать", command=toggle_edit)
edit_btn.pack(side=tk.LEFT, fill='x', expand=True, padx=2)

tk.Button(edit_save_frame, text="Сохранить", command=save_edited_history, bg="#2196F3", fg="white").pack(side=tk.LEFT,
                                                                                                         fill='x',
                                                                                                         expand=True,
                                                                                                         padx=2)

window.mainloop()

