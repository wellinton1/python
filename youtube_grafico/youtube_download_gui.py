import importlib.util
import subprocess
import sys

# Função para verificar se um módulo está instalado
def is_module_installed(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None

# Função para instalar um módulo usando pip
def install_module(module_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

# Verifica e instala os módulos se necessário
required_modules = ["pytube", "tqdm", "moviepy"]
for module in required_modules:
    if not is_module_installed(module):
        print(f"O módulo '{module}' não está instalado. Instalando...")
        install_module(module)

# Importações dos módulos necessários
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import tkinter as tk
from tkinter import ttk, messagebox

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    percentage_of_completion = (bytes_downloaded / total_size) * 100
    progress_bar['value'] = percentage_of_completion
    root.update_idletasks()

def download_video():
    link = entry_link.get()
    resolution = entry_resolution.get()
    output_filename = entry_output.get()
    
    try:
        yt = YouTube(link, on_progress_callback=on_progress)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao obter informações do vídeo: {e}")
        return

    video_stream = yt.streams.filter(res=resolution).first()
    if not video_stream:
        messagebox.showerror("Erro", "Vídeo com a resolução especificada não encontrado.")
        return

    try:
        print("Iniciando download...")
        progress_bar['value'] = 0
        video_stream.download()

        video_path = video_stream.default_filename
        output_path = f"{output_filename}.mp4"

        video_clip = VideoFileClip(video_path)
        video_clip.write_videofile(output_path, codec='libx264')

        os.remove(video_path)  # Remover o arquivo de vídeo original

    except Exception as e:
        messagebox.showerror("Erro", f"Erro durante o download ou conversão: {e}")
    else:
        messagebox.showinfo("Sucesso", "Download e conversão completos.")

# Interface Gráfica
root = tk.Tk()
root.title("Downloader de Vídeos do YouTube")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_link = ttk.Label(frame, text="Link do YouTube:")
label_link.grid(row=0, column=0, sticky=tk.W)

entry_link = ttk.Entry(frame, width=50)
entry_link.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E))

label_resolution = ttk.Label(frame, text="Resolução:")
label_resolution.grid(row=1, column=0, sticky=tk.W)

entry_resolution = ttk.Entry(frame, width=20)
entry_resolution.grid(row=1, column=1, sticky=tk.W)

label_output = ttk.Label(frame, text="Nome do Arquivo de Saída:")
label_output.grid(row=2, column=0, sticky=tk.W)

entry_output = ttk.Entry(frame, width=30)
entry_output.grid(row=2, column=1, sticky=(tk.W, tk.E))

button_download = ttk.Button(frame, text="Baixar", command=download_video)
button_download.grid(row=3, column=1, sticky=tk.W)

progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))

root.mainloop()