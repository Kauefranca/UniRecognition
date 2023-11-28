import requests
import cv2
from os import mkdir, listdir, path
from utils.Camera import Camera

class CapturaFaces:
    def __init__(self, cascade_file):
        # Construtor da classe, recebe o arquivo do classificador e a fonte de vídeo
        self.classificador = cv2.CascadeClassifier(cascade_file)  # Instância do classificador Haar
        self.camera = Camera()  # Instância da câmera de vídeos
        self.amostra = 1
        self.numeroAmostras = 50
        self.capturando = False

    def capturar(self):
        imagem = self.camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        faceDetectadas = self.classificador.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))

        for (x, y, l, a) in faceDetectadas:
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)

            if self.capturando:
                imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (220, 220))
                cv2.imwrite("Fotos/" + str(self.ra) + "/" + str(self.amostra) + ".jpg", imagemFace)
                self.amostra += 1
                cv2.waitKey(50)

                if self.amostra > self.numeroAmostras:
                    self.capturando = False  # Parar a captura após o número desejado de amostras
                    self.incluirNoBanco(self.ra)

        _, jpeg = cv2.imencode('.jpg', imagem)

        return jpeg.tobytes()

    def iniciarCaptura(self, ra):
        mkdir("Fotos/" + ra)
        self.ra = ra
        self.capturando = True
    
    def incluirNoBanco(self, ra):
        url = "http://localhost:5000/incluir_fotos"
        data = {"ra": ra}
        requests.post(url, data=data)

    def __del__(self): # Método destrutor
        del self.camera

if __name__ == "__main__":
    cascade_file = "src\\frontalFaceHaarcascade.xml"  # Arquivo do classificador Haar

    captura = CapturaFaces(cascade_file)  # Instância da classe CapturaFaces
    captura.capturar()  # Chamada do método de captura