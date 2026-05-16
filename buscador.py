import subprocess, sys, webbrowser, urllib.parse, tkinter as tk
from tkinter import messagebox, ttk
import re

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])
    import requests
    from bs4 import BeautifulSoup

def tradutor_inteligente(texto):
    texto = texto.lower()
    dic = {"jazz": "jazz", "smooth": "smooth", "lofi": "lo-fi", "sax": "saxophone"}
    tags = [en for pt, en in dic.items() if pt in texto]
    return " ".join(list(set(tags))) if tags else re.sub(r'[^a-zA-Z0-9 ]', '', texto)

def buscar():
    entrada = entry.get().strip()
    ref_texto = ""
    if entrada:
        if "youtu" in entrada:
            try:
                r = requests.get(entrada.split('&list=')[0], headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                soup = BeautifulSoup(r.text, 'html.parser')
                ref_texto = soup.find('title').text.replace("- YouTube", "").strip()
                ref_texto = tradutor_inteligente(ref_texto)
            except: ref_texto = entrada
        else:
            ref_texto = entrada

    moods_selecionados = [mood for mood, var in moods_vars.items() if var.get()]
    inst_selecionados = [inst for inst, var in inst_vars.items() if var.get()]
    ritmo = vel_var.get()

    busca_artlist = " ".join(list(set([ref_texto] + moods_selecionados + inst_selecionados + [ritmo]))).strip()
    busca_envato = " ".join(list(set([ref_texto] + (moods_selecionados[:2] if moods_selecionados else [])))).strip()

    if not busca_artlist:
        messagebox.showwarning("Aviso", "Selecione algo!")
        return
    
    webbrowser.open(f"https://artlist.io/royalty-free-music/search?terms={urllib.parse.quote_plus(busca_artlist)}")
    webbrowser.open(f"https://elements.envato.com/audio/{urllib.parse.quote_plus(busca_envato)}")

root = tk.Tk()
root.title("BuscaTrilha PRO - Master Edition")
root.geometry("750x850")
root.attributes('-topmost', True)
root.configure(bg="#1A1A1A")

tk.Label(root, text="REFERÊNCIA PRINCIPAL (LINK OU BRIEFING)", fg="#FFD700", bg="#1A1A1A", font=("Arial", 10, "bold")).pack(pady=(20,0))
entry = tk.Entry(root, font=("Arial", 14), bg="#2D2D2D", fg="white", insertbackground="white", bd=0)
entry.pack(fill="x", padx=40, pady=10, ipady=8)

tk.Label(root, text="VELOCIDADE / BPM", fg="#FFD700", bg="#1A1A1A", font=("Arial", 10, "bold")).pack(pady=10)
vel_frame = tk.Frame(root, bg="#1A1A1A")
vel_frame.pack()
vel_var = tk.StringVar(value="medium")
for v in [("LENTA", "slow bpm"), ("MÉDIA", "medium bpm"), ("RÁPIDA", "fast energetic")]:
    tk.Radiobutton(vel_frame, text=v[0], variable=vel_var, value=v[1], indicatoron=0, width=15, selectcolor="#FFD700", bg="#333", fg="black").pack(side="left", padx=5)

tk.Label(root, text="MOODS", fg="#FFD700", bg="#1A1A1A", font=("Arial", 10, "bold")).pack(pady=(20,10))
m_frame = tk.Frame(root, bg="#1A1A1A")
m_frame.pack(padx=40)
moods = ["Uplifting", "Epic", "Powerful", "Happy", "Sad", "Mysterious", "Tense", "Dark", "Peaceful", "Corporate", "Cinematic", "Love", "Aggressive", "Funny", "Groovy", "Playful", "Hopeful", "Serious"]
moods_vars = {}
for i, m in enumerate(moods):
    var = tk.BooleanVar()
    moods_vars[m.lower()] = var
    tk.Checkbutton(m_frame, text=m, variable=var, bg="#1A1A1A", fg="white", selectcolor="#2D2D2D", activebackground="#1A1A1A", activeforeground="white").grid(row=i//3, column=i%3, sticky="w", padx=20, pady=2)

tk.Label(root, text="INSTRUMENTOS", fg="#FFD700", bg="#1A1A1A", font=("Arial", 10, "bold")).pack(pady=(20,10))
i_frame = tk.Frame(root, bg="#1A1A1A")
i_frame.pack(padx=40)
insts = ["Acoustic Guitar", "Electric Guitar", "Piano", "Strings", "Violin", "Cello", "Saxophone", "Flute", "Trumpet", "Drums", "Percussion", "Synth", "Bass", "Orchestra", "Whistle", "Claps", "Bell", "Vocals"]
inst_vars = {}
for i, inst in enumerate(insts):
    var = tk.BooleanVar()
    inst_vars[inst.lower()] = var
    tk.Checkbutton(i_frame, text=inst, variable=var, bg="#1A1A1A", fg="white", selectcolor="#2D2D2D", activebackground="#1A1A1A", activeforeground="white").grid(row=i//3, column=i%3, sticky="w", padx=20, pady=2)

tk.Button(root, text="GERAR BUSCA PROFISSIONAL", font=("Arial", 14, "bold"), bg="#FFD700", fg="black", command=buscar, height=2, width=40, bd=0, cursor="hand2").pack(pady=40)
root.mainloop()
