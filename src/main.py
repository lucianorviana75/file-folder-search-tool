import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import os

# =========================
# Funções
# =========================

def abrir_item(event):
    try:
        selecionado = lista.curselection()
        if not selecionado:
            return
        caminho = caminhos[selecionado[0]]
        os.startfile(caminho)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir:\n{e}")


def escolher_pasta():
    global pasta_escolhida
    pasta_escolhida = filedialog.askdirectory()
    if pasta_escolhida:
        label_pasta.config(text=pasta_escolhida)
        status_var.set("Pasta selecionada. Pronto para buscar.")


def buscar():
    palavra = entry_palavra.get().strip().lower()

    if not palavra:
        messagebox.showwarning("Atenção", "Digite uma palavra-chave.")
        return

    if not pasta_escolhida:
        messagebox.showwarning("Atenção", "Escolha uma pasta para procurar.")
        return

    lista.delete(0, tk.END)
    caminhos.clear()

    raiz = Path(pasta_escolhida)
    contador = 0
    encontrados = 0

    status_var.set("Procurando...")
    janela.update_idletasks()

    try:
        for item in raiz.rglob("*"):
            contador += 1

            # Atualiza o status a cada 100 itens
            if contador % 100 == 0:
                status_var.set(f"Procurando... {contador} itens analisados")
                janela.update_idletasks()

            if palavra in item.name.lower():
                tipo = "PASTA" if item.is_dir() else "ARQUIVO"
                lista.insert(tk.END, f"[{tipo}] {item.name}")
                caminhos.append(str(item))
                encontrados += 1

    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return

    if encontrados == 0:
        lista.insert(tk.END, "Nenhum resultado encontrado.")

    status_var.set(
        f"Busca finalizada. {contador} itens analisados, {encontrados} resultado(s)."
    )


# =========================
# Interface Gráfica
# =========================

janela = tk.Tk()
janela.title("Localizador de Arquivos e Pastas")
janela.geometry("780x520")
janela.resizable(False, False)

pasta_escolhida = ""
caminhos = []

# Palavra-chave
tk.Label(janela, text="Palavra-chave:").pack(anchor="w", padx=10, pady=5)
entry_palavra = tk.Entry(janela, width=40)
entry_palavra.pack(anchor="w", padx=10)

# Pasta
tk.Label(janela, text="Onde procurar:").pack(anchor="w", padx=10, pady=10)
tk.Button(janela, text="Escolher pasta", command=escolher_pasta).pack(anchor="w", padx=10)

label_pasta = tk.Label(
    janela, text="Nenhuma pasta escolhida", fg="gray"
)
label_pasta.pack(anchor="w", padx=10, pady=5)

# Botão buscar
tk.Button(
    janela,
    text="PROCURAR",
    bg="#4CAF50",
    fg="white",
    width=20,
    command=buscar
).pack(pady=15)

# Status
status_var = tk.StringVar()
status_var.set("Pronto.")
label_status = tk.Label(janela, textvariable=status_var, fg="blue")
label_status.pack(pady=5)

# Resultados
tk.Label(
    janela,
    text="Resultados (duplo clique para abrir):"
).pack(anchor="w", padx=10)

lista = tk.Listbox(janela, width=110, height=14)
lista.pack(padx=10, pady=5)

lista.bind("<Double-Button-1>", abrir_item)

janela.mainloop()