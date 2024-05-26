import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import ctypes
import time
import threading

user_password = None
timer_running = False

def lock_screen():
    ctypes.windll.user32.LockWorkStation()

def countdown_timer(seconds):
    global timer_running
    time.sleep(seconds)
    lock_screen()
    timer_running = False

def start_lock_timer():
    global timer_running
    if timer_running:
        messagebox.showwarning("Aviso", "O temporizador já está em execução.")
        return

    try:
        minutes = int(entry_minutes.get())
        if minutes < 0:
            raise ValueError
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()
        
        if password != confirm_password:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        # Salvar a senha
        global user_password
        user_password = password
        
        # Converter minutos para segundos
        seconds = minutes * 60
        
        # Iniciar contagem regressiva em uma nova thread
        timer_running = True
        threading.Thread(target=countdown_timer, args=(seconds,)).start()
        messagebox.showinfo("Timer Iniciado", f"A tela será bloqueada em {minutes} minutos.")
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de minutos.")

def unlock_screen():
    global user_password
    entered_password = simpledialog.askstring("Desbloquear", "Digite a senha:", show='*')
    
    if entered_password == user_password:
        messagebox.showinfo("Desbloqueado", "A tela foi desbloqueada!")
    else:
        messagebox.showerror("Erro", "Senha incorreta!")

def on_closing():
    if user_password is not None:
        entered_password = simpledialog.askstring("Fechar Programa", "Digite a senha para fechar:", show='*')
        if entered_password == user_password:
            root.destroy()
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
    else:
        root.destroy()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Bloquear Tela")
root.iconbitmap("foguete.ico")

tk.Label(root, text="Tempo para bloquear (minutos):").pack(pady=5)
entry_minutes = tk.Entry(root)
entry_minutes.pack(pady=5)

tk.Label(root, text="Digite uma senha:").pack(pady=5)
entry_password = tk.Entry(root, show='*')
entry_password.pack(pady=5)

tk.Label(root, text="Confirme a senha:").pack(pady=5)
entry_confirm_password = tk.Entry(root, show='*')
entry_confirm_password.pack(pady=5)

tk.Button(root, text="Iniciar Timer", command=start_lock_timer).pack(pady=20)
tk.Button(root, text="Desbloquear Tela", command=unlock_screen).pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()