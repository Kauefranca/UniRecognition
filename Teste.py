import tkinter as tk
from tkinter import ttk

class MinhaJanela:
    def __init__(self, root):
        self.root = root
        self.frame_esquerda = ttk.Frame(self.root)
        self.frame_esquerda.pack()

        self.quadrado_centro = ttk.Button(self.frame_esquerda, text="Register", width=50, command=self.capturar)
        self.quadrado_centro.pack(pady=10)

        # Associa eventos de entrada e saída para o botão
        self.quadrado_centro.bind("<Enter>", self.on_enter)
        self.quadrado_centro.bind("<Leave>", self.on_leave)

    def capturar(self):
        print("Botão pressionado!")

    def on_enter(self, event):
        # Define o estilo quando o mouse entra no botão
        self.quadrado_centro.config(style='Hover.TButton')

    def on_leave(self, event):
        # Define o estilo padrão quando o mouse sai do botão
        self.quadrado_centro.config(style='TButton')

root = tk.Tk()

# Cria um estilo para o botão com efeito hovers
style = ttk.Style()
style.configure('Hover.TButton', foreground='red')  # Altere as propriedades de estilo conforme desejado

app = MinhaJanela(root)
root.mainloop()
