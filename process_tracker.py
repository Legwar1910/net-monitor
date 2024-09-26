import psutil
import os
import tkinter as tk
from tkinter import messagebox

# Функція перевірки існування процесу за його ID
def check_process(pid):
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False

# Функція для гібернації комп'ютера
def hibernate():
    if os.name == 'nt':  # Для Windows
        os.system("shutdown /h")
    else:
        messagebox.showerror("Помилка", "Гібернація підтримується тільки на Windows")

# Функція для завершення роботи комп'ютера
def shutdown():
    if os.name == 'nt':  # Для Windows
        os.system("shutdown /s /t 1")
    else:
        messagebox.showerror("Помилка", "Завершення роботи підтримується тільки на Windows")

# Функція для перезавантаження комп'ютера
def restart():
    if os.name == 'nt':  # Для Windows
        os.system("shutdown /r /t 1")
    else:
        messagebox.showerror("Помилка", "Перезавантаження підтримується тільки на Windows")

# Функція для виконання обраної дії
def execute_action(action):
    if action == "Гібернація":
        hibernate()
    elif action == "Завершення роботи":
        shutdown()
    elif action == "Перезавантаження":
        restart()
    elif action == "Нічого не робити":
        messagebox.showinfo("Інформація", "Процес завершився, жодних дій не виконується.")
    else:
        messagebox.showerror("Помилка", "Невідома дія.")

# Функція, яка перевіряє процес і чекає його завершення
def monitor_process():
    try:
        pid = int(entry_pid.get())
        if not check_process(pid):
            messagebox.showerror("Помилка", "Процес з таким ID не існує.")
            return

        messagebox.showinfo("Інформація", f"Моніторимо процес з ID: {pid}")

        # Очікуємо завершення процесу
        while check_process(pid):
            window.update()  # Оновлення інтерфейсу

        messagebox.showinfo("Інформація", "Процес завершився. Виконуємо вибрану дію.")
        execute_action(action_var.get())  # Виконати вибрану користувачем дію
    except ValueError:
        messagebox.showerror("Помилка", "Введіть коректний ID процесу.")

# Створення графічного інтерфейсу
window = tk.Tk()
window.title("Моніторинг процесу")
window.geometry("300x250")

# Написи і поля для введення
label_pid = tk.Label(window, text="Введіть ID процесу:")
label_pid.pack(pady=5)

entry_pid = tk.Entry(window)
entry_pid.pack(pady=5)

# Створення меню для вибору дії після завершення процесу
label_action = tk.Label(window, text="Виберіть дію після завершення процесу:")
label_action.pack(pady=5)

action_var = tk.StringVar(window)
action_var.set("Гібернація")  # Значення за замовчуванням

# Опції для вибору
action_menu = tk.OptionMenu(window, action_var, "Гібернація", "Завершення роботи", "Перезавантаження", "Нічого не робити")
action_menu.pack(pady=5)

# Кнопка для запуску моніторингу
btn_monitor = tk.Button(window, text="Моніторити", command=monitor_process)
btn_monitor.pack(pady=10)

# Запуск інтерфейсу
window.mainloop()
