
#IMPORT
import tkinter as tk
from tkinter import messagebox
import json

#FUNCTIONS
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
        except(FileNotFoundError, json.JSONDecodeError):
            return 0, []

#WIDGET FUNCTIONS

def update_sidebar():
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


def add_income():
        global balance
        try:
            money = float(money_entry.get())
            balance = balance + money
            history.append(f"Income +{money}$")
            save_data()
            balance_label.config(text = f"Balance {balance}$")
            money_entry.delete(0, tk.END)
            update_sidebar()


        except ValueError:
            messagebox.showerror("Error!", "Input Error. Invalid symbol entered in the field.")



def add_expense():
    global balance
    try:
        money = float(money_entry.get())

        if money > balance:
            messagebox.showerror("Balance Error" , f"Amount is too large.\n{money}$")
            return

        balance = balance - money
        history.append(f"Expense - {money}$")
        save_data()
        balance_label.config(text = f"Balance {balance}$")
        money_entry.delete(0, tk.END)
        update_sidebar()


    except ValueError:
        messagebox.showerror("Error!", "Input Error. Invalid symbol entered in the field.")


def toggle_edit():

    global global_history_area
    current_state = global_history_area.cget("state")
    if current_state == tk.DISABLED:
            global_history_area.config(state=tk.NORMAL)
            messagebox.showinfo("Success!", "Editing enabled")
    else:
        global_history_area.config(state=tk.DISABLED)
        messagebox.showinfo("Success!", "Editing disabled")



def save_edited_history():
        global balance
        global history

        balance = 0
        history = []

        full_text = global_history_area.get(1.0, tk.END).strip()

        if not full_text:
            save_data()
            update_sidebar()
            balance_label.config(text=f"Balance: {balance}$")
            return

        new_line = full_text.split("\n")
        for line in new_line:
            line = line.strip()
            if not line: continue

            parts = line.split(" ")
            history.append(line)

            amount = 0
            found_money = False

            for part in parts:
                clean_part = part.replace("$", "").replace('-', '').replace('+', '')

                if clean_part.replace('.','',1).isdigit():
                    amount = float(clean_part)
                    found_money = True
                    break


            if found_money:
                if line.startswith("Income"):
                    balance += amount

                elif line.startswith("Expense"):
                    balance -= amount


        save_data()
        update_sidebar()
        balance_label.config(text=f"Balance {balance}$")
        global_history_area.config(state=tk.DISABLED)
        messagebox.showinfo("Success", "Balance recalculated and saved!")




#ЗАГРУЗКА ДАННЫХ
balance, history = load_data()
global_history_area= None


#ОКОШКО
window = tk.Tk()
window.title("Finance tracker")
window.geometry("800x600")
window.minsize(800, 600)
window.maxsize(800, 600)


#СТРУКТУРА ОКНА

top_frame = tk.Frame(window)
top_frame.pack(side=tk.TOP, fill=tk.X,
               padx=10, pady=10)

main_container = tk.Frame(window)
main_container.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_container)
left_frame.pack(side=tk.LEFT,fill=tk.BOTH,
                expand=True, padx=10)

right_frame = tk.Frame(main_container, width=400, bg="#f0f0f0")


money_entry = tk.Entry(left_frame, font=("Arial", 20))
money_entry.pack(pady=20, fill='x')

# Контейнер для текста

text_frame = tk.Frame(right_frame)
text_frame.pack(pady=10, padx=10, expand=True)

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

edit_save_frame = tk.Frame(right_frame,width=350)
edit_save_frame.pack(side=tk.BOTTOM, fill='x', pady=5)
tk.Button(edit_save_frame, text="Edit",
          command=toggle_edit).pack(side=tk.LEFT, fill='x', expand=True)

tk.Button(edit_save_frame, text="Save",
          command=save_edited_history,bg="#2196F3", fg="white").pack(side=tk.LEFT, fill='x', expand=True)

show_history_var = tk.BooleanVar()
show_history_var.set(False)

#Элементики мои маленькие
balance_label = tk.Label(top_frame, text=f"Balance {balance}$" , font=("Arial", 20))
balance_label.pack(pady=20, fill='x')

history_checkbox = tk.Checkbutton(top_frame, text="Show history",
                                  variable= show_history_var,
                                  command=toggle_history_panel)
history_checkbox.pack(side=tk.RIGHT, padx=10)


#САМИ КНОПКИ
button_frame = tk.Frame(left_frame)
button_frame.pack(pady=20, fill='x')



income_btn = tk.Button(button_frame, text="➕Add income" ,
                command=add_income, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), height=2,
                    )

income_btn.pack(side = tk.LEFT, padx=(5,0),fill='x', expand=True)


expense_btn = tk.Button(
    button_frame, text= "➖Add Expense" ,
    command=add_expense ,bg="#F44336", fg="white", font=("Arial", 11, "bold"), height=2,
    )

expense_btn.pack(side = tk.RIGHT, padx=(5,0), fill='x', expand=True)





#ЗАПУСК
window.mainloop()
