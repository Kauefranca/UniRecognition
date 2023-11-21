import tkinter as tk
from tkinter import ttk

class SeuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FaceRecognition")

        # Frames
        self.frame_esquerda = ttk.Frame(root, padding="10")
        self.frame_esquerda.grid(row=0, column=0, sticky="nsew")

        self.frame_direita = ttk.Frame(root, padding="10")
        self.frame_direita.grid(row=0, column=3, sticky="nsew")

        # Configuração das colunas e linhas para expansão
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        self.criar_layout_esquerda()
        self.criar_layout_direita()

    def criar_layout_esquerda(self):
        # Quadrado superior à esquerda
        quadrado_superior = ttk.Label(self.frame_esquerda, text="Video error", width=100, borderwidth=3, background="black")
        quadrado_superior.grid(row=0, column=0, pady=10, ipady=175)

        # Quadrado centro à esquerda
        quadrado_centro = ttk.Button(self.frame_esquerda, text="Register", width=50)
        quadrado_centro.grid(row=1, column=0, pady=10, ipady=10)

        # Quadrado centro à esquerda
        quadrado_centro = ttk.Button(self.frame_esquerda, text="Training", width=50)
        quadrado_centro.grid(row=2, column=0, pady=1, ipady=10)

    def criar_layout_direita(self):
        # Espaço para exibir informações do banco de dados
        info_banco_dados = ttk.Label(self.frame_direita, relief="solid", text="Informações do Banco de Dados", font=("Arial", 14))
        info_banco_dados.grid(row=0, column=0, pady=10, ipady=300 )

        # Adicione aqui widgets ou outros elementos para exibir informações do banco de dados

if __name__ == "__main__":
    root = tk.Tk()
    root.title("UniRecognition")
    root.geometry('920x660')
    root.minsize(920, 660) 
    root.maxsize(920, 660) 
    app = SeuApp(root)
    root.mainloop()
