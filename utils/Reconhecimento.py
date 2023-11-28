from math import floor
import cv2
from utils.Camera import Camera

class ReconhecimentoFacial: # Classe
    def __init__(self, classifier_file, recognizer_file): # Método construtor
        self._classificador = cv2.CascadeClassifier(classifier_file) # Atributo protegido
        self.reconhecedor = cv2.face.LBPHFaceRecognizer_create()
        self.reconhecedor.read(recognizer_file)
        self.camera = Camera()

    # @staticmethod
    def run(self): # Métodos
        # while True:
        imagem = self.camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        faceDetectadas = self._classificador.detectMultiScale(imagemCinza, scaleFactor=1.5)

        for (x, y, l, a) in faceDetectadas:
            imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (100, 100))
            
            id, confianca = self.reconhecedor.predict(imagemFace)

            cor = (0, 0, 255)

            if confianca < 79 and id in self.alunos:
                nome = f"{self.alunos[id]} {str(floor(confianca))}"
                cor = (0, 255, 0)
            else:
                nome = "Esquisito"

            cv2.rectangle(imagem, (x, y), (x + l, y + a), cor, 2)
            cv2.putText(imagem, nome, (x, y + a + 30), cv2.FONT_HERSHEY_TRIPLEX, 1, cor)

        # cv2.imshow("UniRecognition", imagem)

        cv2.waitKey(1)
        _, jpeg = cv2.imencode('.jpg', imagem)

        return jpeg.tobytes()

        # return imagem
            
            # if cv2.waitKey(1) == ord('q'):
            #     break

    @property
    def verAlunos(self):
        print("Acessando a lista de alunos...")
        return self.alunos
    
    def setAlunos(self, alunos):
        self.alunos = alunos

    def __del__(self): # Método destrutor
        del self.camera
        print("Objeto ReconhecimentoFacial destruído")

if __name__ == "__main__":
    classifier_file = 'src\\frontalFaceHaarcascade.xml'
    recognizer_file = 'src\\classificadores\\BCCA.yml'

    reconhecimento = ReconhecimentoFacial(classifier_file, recognizer_file)
    reconhecimento.setAlunos({
  "1964011": "Kaue"})
    reconhecimento.run()