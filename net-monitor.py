import json
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import subprocess
from scapy.all import *

# Шлях до файлу з налаштуваннями та версією
settings_file = 'settings.json'
version_file = 'version.txt'
version_url = 'https://github.com/yourusername/yourrepo/raw/main/version.txt'  # Змініть на URL до вашого файлу з версією на GitHub

# Функція для завантаження налаштувань
def load_settings():
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            return settings
    except FileNotFoundError:
        return {'last_interface': None, 'allowed_ips': [], 'blocked_ips': [], 'version': '0.0.0'}

# Функція для збереження налаштувань
def save_settings(interface, allowed_ips, blocked_ips, version):
    with open(settings_file, 'w') as f:
        json.dump({
            'last_interface': interface,
            'allowed_ips': allowed_ips,
            'blocked_ips': blocked_ips,
            'version': version
        }, f)

# Глобальні змінні для дозволених і не дозволених IP
allowed_ips = []
blocked_ips = []
current_version = '1.0.0'  # Поточна версія програми

def check_for_updates():
    try:
        response = requests.get(version_url)
        latest_version = response.text.strip()
        if latest_version != current_version:
            return latest_version
    except Exception as e:
        print(f"Error checking for updates: {e}")
    return None

def update_program():
    latest_version = check_for_updates()
    if latest_version:
        messagebox.showinfo("Update Available", f"A new version ({latest_version}) is available!")
        # Тут можна реалізувати логіку завантаження та оновлення програми
        # Наприклад, ви можете використовувати команду для завантаження нового файлу:
        # subprocess.call(['curl', '-O', f'https://github.com/yourusername/yourrepo/releases/download/{latest_version}/yourprogram.exe'])
        # Замініть це на реальну логіку оновлення програми
        messagebox.showinfo("Update", "Please download and install the latest version manually.")
    else:
        messagebox.showinfo("No Update", "You are already using the latest version.")

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        if ip_src in blocked_ips:
            print(f"Blocked IP detected: {ip_src}")
        elif ip_src in allowed_ips:
            print(f"Allowed IP detected: {ip_src}")

def start_monitoring(interface):
    global monitoring
    if interface not in get_if_list():
        messagebox.showerror("Error", f"Interface '{interface}' does not exist.")
        return
    monitoring = True
    print(f"Starting network monitoring on interface: {interface}")
    sniff(iface=interface, prn=packet_callback, filter="ip", stop_filter=lambda p: not monitoring)

def stop_monitoring():
    global monitoring
    monitoring = False
    print("Stopping network monitoring")

def on_start_button_click():
    selected_iface = iface_combobox.get()
    if selected_iface not in get_if_list():
        messagebox.showerror("Error", f"Interface '{selected_iface}' does not exist.")
        return
    save_settings(selected_iface, allowed_ips, blocked_ips, current_version)
    start_monitoring(selected_iface)

def on_stop_button_click():
    stop_monitoring()

def update_ip_lists():
    global allowed_ips, blocked_ips
    allowed_ips = [ip.strip() for ip in allowed_ip_text.get("1.0", "end-1c").split('\n') if ip.strip()]
    blocked_ips = [ip.strip() for ip in blocked_ip_text.get("1.0", "end-1c").split('\n') if ip.strip()]
    save_settings(iface_combobox.get(), allowed_ips, blocked_ips, current_version)

# Створення графічного інтерфейсу
root = tk.Tk()
root.title("Network Monitor")

# Отримання списку інтерфейсів та налаштувань
interfaces = get_if_list()
settings = load_settings()
last_interface = settings.get('last_interface')
allowed_ips = settings.get('allowed_ips', [])
blocked_ips = settings.get('blocked_ips', [])
current_version = settings.get('version', '1.0.0')

# Поля вводу для IP-адрес
tk.Label(root, text="Allowed IP addresses (one per line):").pack(pady=5)
allowed_ip_text = tk.Text(root, height=10, width=40)
allowed_ip_text.insert("1.0", "\n".join(allowed_ips))
allowed_ip_text.pack(pady=5)

tk.Label(root, text="Blocked IP addresses (one per line):").pack(pady=5)
blocked_ip_text = tk.Text(root, height=10, width=40)
blocked_ip_text.insert("1.0", "\n".join(blocked_ips))
blocked_ip_text.pack(pady=5)

# Компоненти для вибору інтерфейсу
tk.Label(root, text="Select network interface:").pack(pady=5)
iface_combobox = ttk.Combobox(root, values=interfaces)
iface_combobox.set(last_interface if last_interface in interfaces else "Select network interface")
iface_combobox.pack(pady=5)

# Кнопки для керування моніторингом
start_button = tk.Button(root, text="Start Monitoring", command=lambda: [update_ip_lists(), on_start_button_click()])
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Monitoring", command=on_stop_button_click)
stop_button.pack(pady=5)

# Кнопка для оновлення програми
update_button = tk.Button(root, text="Check for Updates", command=update_program)
update_button.pack(pady=10)

root.mainloop()
