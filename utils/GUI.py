import tkinter as tk
from tkinter import ttk

class SeuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Layout Tkinter com Banco de Dados")

        # Frames
        self.frame_esquerda = ttk.Frame(root, padding="10")
        self.frame_esquerda.grid(row=0, column=0, sticky="nsew")

        self.frame_direita = ttk.Frame(root, padding="10")
        self.frame_direita.grid(row=0, column=1, sticky="nsew")

        # Configuração das colunas e linhas para expansão
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        self.criar_layout_esquerda()
        self.criar_layout_direita()

    def criar_layout_esquerda(self):
        # Quadrado superior à esquerda
        quadrado_superior = ttk.Label(self.frame_esquerda, text="Quadrado Superior", background="lightblue")
        quadrado_superior.grid(row=0, column=0, pady=10)

        # Quadrado inferior à esquerda
        quadrado_inferior = ttk.Label(self.frame_esquerda, text="Quadrado Inferior", background="lightgreen")
        quadrado_inferior.grid(row=1, column=0, pady=10)

    def criar_layout_direita(self):
        # Espaço para exibir informações do banco de dados
        info_banco_dados = ttk.Label(self.frame_direita, text="Informações do Banco de Dados", font=("Helvetica", 14))
        info_banco_dados.grid(row=0, column=0, pady=10)

        # Adicione aqui widgets ou outros elementos para exibir informações do banco de dados

if __name__ == "__main__":
    root = tk.Tk()
    root.title("UniRecognition")
    root.geometry('920x660')
    app = SeuApp(root)
    root.mainloop()
