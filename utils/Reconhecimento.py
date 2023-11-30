import cv2
import psycopg2
from math import floor
from datetime import datetime as dt

from utils.Camera import Camera

con = psycopg2.connect(
	host='localhost', 
	database='postgres', 
	port='5432',
	user='postgres', 
	password='unimar'
)

entrada = []
saida = []

class ReconhecimentoFacial: # Classe
    def __init__(self, classifier_file, recognizer_file): # Método construtor
        self._classificador = cv2.CascadeClassifier(classifier_file) # Atributo protegido
        self.reconhecedor = cv2.face.LBPHFaceRecognizer_create()
        self.reconhecedor.read(recognizer_file)
        self.status = None
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

            if confianca < 79:
                if self.status == 'entrada':
                    cursor = con.cursor()
                    sql = """UPDATE registro SET entrada=current_timestamp WHERE id_aluno=((SELECT id_aluno FROM aluno WHERE ra = %s)) AND entrada IS NULL;"""
                    cursor.execute(sql, (id,))
                    con.commit()
                elif self.status == 'saida':
                    if id not in saida:
                        cursor = con.cursor()
                        sql = """UPDATE registro SET saida=current_timestamp WHERE id_aluno=((SELECT id_aluno FROM aluno WHERE ra = %s)) AND saida IS NULL;"""
                        cursor.execute(sql, (id,))
                        con.commit()

                nome = f"{id} {str(floor(confianca))}"
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

    def setStatus(self, status):
        self.status = status

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