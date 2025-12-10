import tkinter as tk
from tkinter import messagebox
import json

# --- #ФУНКЦИИ (ВСЕ ФУНКЦИИ НАВЕРХУ) ---

def save_data():
    data = {
    "balance" : balance,
    "history": history,
         }
    with open("data.json" ,"w", encoding="utf-8" ) as json_file:
        json.dump(data,json_file,ensure_ascii=False, indent=4)


def load_data():
        try:
            with open("data.json", "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                return data["balance"], data["history"]
        except:
            return 0, []


# ✅ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (ДОЛЖНЫ БЫТЬ ОПРЕДЕЛЕНЫ РАНЬШЕ)

def update_sidebar():
    # Проверка, чтобы избежать NameError при первом запуске
    if 'global_history_area' in globals() and global_history_area:
        global_history_area.config(state=tk.NORMAL)
        global_history_area.delete(1.0, tk.END)

        history_text = "\n".join(history)
        global_history_area.insert(tk.END, history_text)

        global_history_area.config(state=tk.DISABLED)


def open_sidebar_from_button():
    show_history_var.set(True)
    toggle_history_panel()


def toggle_history_panel():
    if show_history_var.get():
        right_frame.pack(side=tk.RIGHT,
                         fill=tk.BOTH, padx=10)
        update_sidebar()
    else:
        right_frame.pack_forget()


# ФУНКЦИИ ДЛЯ КНОПОЧЕК

def add_income():
        global balance
        try:
            money = float(money_entry.get())
            balance = balance + money
            history.append(f"Доход +{money}$")
            save_data()
            balance_label.config(text = f"Баланс {balance}$")
            money_entry.delete(0, tk.END)
            update_sidebar()


        except ValueError:
            messagebox.showerror("Ошибка!", "Ошибка ввода. В поле введен неправильный символ.")



def add_expense():
    global balance
    try:
        money = float(money_entry.get())

        if money > balance:
            messagebox.showerror("Ошибка баланса" , f"Слишком большая сумма.\n{money}$")
            return

        balance = balance - money
        history.append(f"Расход - {money}$")
        save_data()
        balance_label.config(text = f"Баланс {balance}$")
        money_entry.delete(0, tk.END)
        update_sidebar()


    except ValueError:
        messagebox.showerror("Ошибка!", "Ошибка ввода. В поле введен неправильный символ.")


def toggle_edit():

    global global_history_area
    current_state = global_history_area.cget("state")
    if current_state == tk.DISABLED:
            global_history_area.config(state=tk.NORMAL)
            messagebox.showinfo("Успешно", "Редактирование включено")
    else:
        global_history_area.config(state=tk.DISABLED)
        messagebox.showinfo("Успешно", "Редактирование Отключено")



def save_edited_history():
        global balance
        global history

        balance = 0
        history = []

        full_text = global_history_area.get(1.0, tk.END + '-1c')
        new_line = full_text.split("\n")

        for line in new_line:

            if line.startswith("Расход"):
                parts = line.split(' ')
                history.append(line)
                if len(parts) > 1:
                    amount_str = parts[1].replace('$', '')
                    amount = float(amount_str)
                    balance = balance - amount

            elif line.startswith("Доход"):
                parts = line.split(' ')
                history.append(line)
                if len(parts) > 1:
                    amount_str = parts[1].replace('$', '')
                    amount = float(amount_str)
                    balance = balance + amount
            elif line.strip() != "":
                history.append(line)


        save_data()
        update_sidebar()
        balance_label.config(text=f"Баланс {balance}$")
        global_history_area.config(state=tk.DISABLED)
        messagebox.showinfo("Успешно", "Баланс пересчитан и сохранен!")

# --- КОНЕЦ БЛОКА ФУНКЦИЙ ---


#ЗАГРУЗКА ДАННЫХ
balance, history = load_data()
global_history_area= None


#ОКОШКО
window = tk.Tk()
window.title("Электронный Кошелек")
window.state('zoomed')

#СТРУКТУРА ОКНА

top_frame = tk.Frame(window)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

main_container = tk.Frame(window)
main_container.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_container)
left_frame.pack(side=tk.LEFT,fill=tk.BOTH, expand=True, padx=10)

right_frame = tk.Frame(main_container, width=400, bg="#f0f0f0")

# --- СОЗДАНИЕ ПЕРЕМЕННЫХ ---
show_history_var = tk.BooleanVar()
show_history_var.set(False)

# --- ЭЛЕМЕНТЫ TOP_FRAME ---
balance_label = tk.Label(top_frame, text=f"Баланс {balance}$" , font=("Arial", 20))
balance_label.pack(side=tk.LEFT, pady=20, fill='x')

history_checkbox = tk.Checkbutton(top_frame, text="Показать историю",
                      variable=show_history_var,
                      command=toggle_history_panel)
history_checkbox.pack(side=tk.RIGHT, padx=10)

# --- ЭЛЕМЕНТЫ LEFT_FRAME ---
tk.Label(left_frame, text="Финансовый Отчет", font=("Arial", 20)).pack(fill='x')
money_entry = tk.Entry(left_frame, font=("Arial", 20))
money_entry.pack(pady=20, fill='x')


# --- ЭЛЕМЕНТЫ RIGHT_FRAME (САЙДБАР) ---
# Контейнер для текста
text_frame = tk.Frame(right_frame)
text_frame.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

# Поле для прокрутки
scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Связывание Scrollbar с Text
global_history_area = tk.Text(
    text_frame,
    wrap=tk.WORD,
    yscrollcommand=scrollbar.set,
    font=("Arial", 10)
)
global_history_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=global_history_area.yview)

# Вставки данных и защита от случайного редактирования
global_history_area.config(state=tk.DISABLED)

edit_save_frame = tk.Frame(right_frame)
edit_save_frame.pack(side=tk.BOTTOM, fill='x', pady=5)
tk.Button(edit_save_frame, text="Редактировать",
          command=toggle_edit).pack(side=tk.LEFT, padx=10, expand=True)

tk.Button(edit_save_frame, text="Сохранить",
          command=save_edited_history).pack(side=tk.LEFT, padx=10, expand=True)


#САМИ КНОПКИ (ВНУТРИ LEFT_FRAME)
button_frame = tk.Frame(left_frame)
button_frame.pack(pady=20, fill='x')


income_btn = tk.Button(button_frame, text="Добваить доход" ,
                command=add_income, bg="green", fg="white" ,
                font=("Arial", 12 ))
income_btn.pack(side = tk.LEFT, padx=10, fill='x', expand=True)


expence_btn = tk.Button(
    button_frame, text= "Добавить расход",
    command=add_expense ,bg="red", fg="white" ,
    font=("Arial", 12 ))
expence_btn.pack(side = tk.LEFT, padx=10, fill='x', expand=True)


history_btn = tk.Button(
    button_frame, text="История",
    command=open_sidebar_from_button, bg="blue", fg="white",
    font=("Arial", 12 ))
history_btn.pack(side = tk.LEFT, padx=10, fill='x', expand=True)


#ЗАПУСК
window.mainloop()