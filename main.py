import cv2
import json

class ReconhecimentoFacial: # Classe
    def __init__(self, aluno_data_file, classifier_file, recognizer_file, video_source): # Método construtor
        # Atributos
        self.__alunos = self.carregar_alunos(aluno_data_file) # Atributo privado
        self._classificador = cv2.CascadeClassifier(classifier_file) # Atributo protegido
        self._reconhecedor = cv2.face.LBPHFaceRecognizer_create() # Atributo protegido
        self._reconhecedor.read(recognizer_file) # Atributo protegido
        self.__camera = cv2.VideoCapture(video_source) # Atributo privado

    def carregar_alunos(self, aluno_data_file): # Método
        with open(aluno_data_file) as f:
            return json.load(f)

    def run(self): # Método
        while True:
            conectado, imagem = self.__camera.read()
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            faceDetectadas = self._classificador.detectMultiScale(imagemCinza, scaleFactor=1.5)

            for (x, y, l, a) in faceDetectadas:
                imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (100, 100))
                cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
                id, confianca = self._reconhecedor.predict(imagemFace)

                if str(id) in self.__alunos:
                    nome = self.__alunos[str(id)]
                else:
                    nome = "Desconhecido"

                cv2.putText(imagem, nome, (x, y + a + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))

            cv2.imshow("Face", imagem)
            if cv2.waitKey(1) == ord('q'):
                break

    def __del__(self): # Método destrutor
        self.__camera.release()
        cv2.destroyAllWindows()
        print("Objeto ReconhecimentoFacial destruído")

if __name__ == "__main__":
    aluno_data_file = 'BCC-A.json'
    classifier_file = 'haarcascade_frontalface_default.xml'
    recognizer_file = 'classificadorLBPH_V1.yml'
    video_source = 'http://192.168.68.104:4747/video'


    reconhecimento = ReconhecimentoFacial(aluno_data_file, classifier_file, recognizer_file, video_source)
    reconhecimento.run()

    print(ReconhecimentoFacial._atributo_protegido)  # Acesso ao atributo protegido

