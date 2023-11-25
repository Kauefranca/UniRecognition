import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
from queue import Queue, Empty
import sys
import cv2
from Reconhecimento import ReconhecimentoFacial
from PIL import Image, ImageTk

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

        
        aluno_data_file = 'salas\\BCC\\2A.json'
        classifier_file = 'src\\frontalFaceHaarcascade.xml'
        recognizer_file = 'src\\classificadores\\classificadorLBPH_V1.yml'

        self.reconhecimento = ReconhecimentoFacial(aluno_data_file, classifier_file, recognizer_file)


        self.iniciar_camera()

    def criar_layout_esquerda(self):
        # Camera superior
        self.canvas_camera = tk.Canvas(self.frame_esquerda, width=650, height=350)
        self.canvas_camera.grid(row=0, column=0, pady=5, ipady=10)

        # Quadrado centro à esquerda
        quadrado_centro = ttk.Button(self.frame_esquerda, text="Register", width=50)
        quadrado_centro.grid(row=1, column=0, pady=10, ipady=10)

        # Quadrado centro à esquerda
        quadrado_centro = ttk.Button(self.frame_esquerda, text="Training", width=50)
        quadrado_centro.grid(row=2, column=0, pady=10, ipady=10)

    def iniciar_camera(self):
        self.thread_running = True
        self.camera_thread = threading.Thread(target=self.atualizar_feed_camera)
        self.camera_thread.start()

    def parar_camera(self):
        self.thread_running = False
        if self.camera_thread:
            self.camera_thread.join()

    def atualizar_feed_camera(self):
        while self.thread_running:
            # frame = self.cap()
            # if frame:
                # Converta o frame para o formato do Tkinter
            frame = cv2.cvtColor(self.reconhecimento.run(), cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            # Atualize o widget Canvas com o novo framef
            self.canvas_camera.imgtk = imgtk
            self.canvas_camera.create_image(0, 0, anchor=tk.NW, image=imgtk)
            
    def criar_layout_direita(self):
        # Espaço para exibir informações do banco de dados
        info_banco_dados = ttk.Label(self.frame_direita, text="Informações do Banco de Dados", font=("Arial", 14))
        info_banco_dados.grid(row=0, column=0, pady=1, ipady=10)

        # Text widget para exibir informações em tempo real
        self.text_terminal = ScrolledText(self.frame_direita, wrap="word", height=27, width=40)
        self.text_terminal.grid(row=1, column=0, pady=10)

        # Adicione aqui widgets ou outros elementos para exibir informações do banco de dados

        # Criar uma fila para passar mensagens entre threads
        self.queue = Queue()

        # Iniciar a thread para exibir mensagens em tempo real
        self.thread = threading.Thread(target=self.update_text_from_queue)
        self.thread.daemon = True
        self.thread.start()

        # Redireciona a saída padrão para a função que coloca mensagens na fila
        sys.stdout = self.TkinterRedirector(self.queue.put)

    def update_text_from_queue(self):
        while True:
            try:
                msg = self.queue.get(timeout=0.1)
                if msg is None:  # Sinal para encerrar a thread
                    break
                self.text_terminal.insert(tk.END, msg)
                self.text_terminal.see(tk.END)  # Rolagem automática para a parte inferior
            except Empty:  # Correção aqui
                pass

    class TkinterRedirector:
        def __init__(self, callback):
            self.callback = callback

        def write(self, text):
            self.callback(text)

        def flush(self):
            pass

    def obter_informacoes_banco_dados(self):
        # Simulação: substitua isso com a lógica real para obter as informações do banco de dados
        informacoes = "Informações do banco de dados:\n"

        #self.info_banco_dados.config(text=informacoes)
        self.queue.put(informacoes)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("UniRecognition")
    root.geometry('985x530')
    #root.minsize(985, 530)
    #root.maxsize(985, 530)
    app = SeuApp(root)
    app.obter_informacoes_banco_dados()
    root.mainloop()

    # Terminar a thread quando a janela for fechada
    app.queue.put(None)
    app.thread.join()