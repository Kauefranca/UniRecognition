from math import floor
import cv2
import json
from Camera import Camera

class ReconhecimentoFacial: # Classe
    def __init__(self, aluno_data_file, classifier_file, recognizer_file): # Método construtor
        self.alunos = self.carregar_alunos(aluno_data_file)
        self._classificador = cv2.CascadeClassifier(classifier_file) # Atributo protegido
        self.reconhecedor = cv2.face.LBPHFaceRecognizer_create()
        self.reconhecedor.read(recognizer_file)
        self.camera = Camera()

    @staticmethod
    def carregar_alunos(aluno_data_file): # Método
        with open(aluno_data_file) as f:
            return json.load(f)

    # @staticmethod
    def run(self): # Método
        #while True:
        imagem = self.camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        faceDetectadas = self._classificador.detectMultiScale(imagemCinza, scaleFactor=1.5)

        for (x, y, l, a) in faceDetectadas:
            imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (100, 100))
            
            id, confianca = self.reconhecedor.predict(imagemFace)

            cor = (0, 0, 255)


            if confianca < 79 and str(id) in self.alunos:
                nome = f"{self.alunos[str(id)]} {str(floor(confianca))}"
                cor = (0, 255, 0)
            else:
                nome = "Desconhecido"

            cv2.rectangle(imagem, (x, y), (x + l, y + a), cor, 2)
            cv2.putText(imagem, nome, (x, y + a + 30), cv2.FONT_HERSHEY_TRIPLEX, 1, cor)

        return imagem
            
            #cv2.imshow("UniRecognition", imagem)
            #if cv2.waitKey(1) == ord('q'):
                #break

    @property
    def verAlunos(self):
        print("Acessando a lista de alunos...")
        return self.alunos

    def __del__(self): # Método destrutor
        del self.camera
        print("Objeto ReconhecimentoFacial destruído")

if __name__ == "__main__":
    aluno_data_file = 'salas\\BCC\\2A.json'
    classifier_file = 'src\\frontalFaceHaarcascade.xml'
    recognizer_file = 'src\\classificadores\\classificadorLBPH_V1.yml'

    reconhecimento = ReconhecimentoFacial(aluno_data_file, classifier_file, recognizer_file)
    reconhecimento.run()