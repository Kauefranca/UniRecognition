import cv2
from Camera import Camera

class CapturaFaces:
    def __init__(self, cascade_file):
        # Construtor da classe, recebe o arquivo do classificador e a fonte de vídeo
        self.classificador = cv2.CascadeClassifier(cascade_file)  # Instância do classificador Haar
        self.camera = Camera()  # Instância da câmera de vídeo
        self.amostra = 1
        self.numeroAmostras = 25
        self.ra = input("Digite seu identificador: ")

    def capturar(self):
        # Método para capturar as faces
        capturando = False
        while True:
            imagem = self.camera.read()
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            faceDetectadas = self.classificador.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))

            for (x, y, l, a) in faceDetectadas:
                cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    capturando = True  # Iniciar a captura apenas quando 'c' for pressionado

                if capturando:
                    imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (220, 220))
                    cv2.imwrite("Fotos/pessoa." + str(self.ra) + "." + str(self.amostra) + ".jpg", imagemFace)
                    print("[Foto " + str(self.amostra) + " capturada com sucesso]")
                    self.amostra += 1

                    if self.amostra > self.numeroAmostras:
                        capturando = False  # Parar a captura após o número desejado de amostras

            cv2.imshow("Face", imagem)
            cv2.waitKey(1)
            if self.amostra > self.numeroAmostras:
                break

        print("Faces capturadas com sucesso")

    def fechar(self):
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cascade_file = "src\\frontalFaceHaarcascade.xml"  # Arquivo do classificador Haar

    captura = CapturaFaces(cascade_file)  # Instância da classe CapturaFaces
    captura.capturar()  # Chamada do método de captura
    captura.fechar()  # Chamada do método de fechamento de recursos
