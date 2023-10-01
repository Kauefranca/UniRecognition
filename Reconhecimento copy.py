import cv2
import json

class Aluno:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return f"Aluno: {self.nome}"

class ReconhecimentoFacial: # Classe
    def __init__(self, aluno_data_file, classifier_file, recognizer_file, video_source): # Método construtor
        # Atributos
        self.alunos = self.carregar_alunos(aluno_data_file)
        self._classificador = cv2.CascadeClassifier(classifier_file) # Atributo protegido
        self.reconhecedor = cv2.face.LBPHFaceRecognizer_create()
        self.reconhecedor.read(recognizer_file)
        self.camera = cv2.VideoCapture(video_source)

    def carregar_alunos(self, aluno_data_file): # Método
        with open(aluno_data_file) as f:
            return json.load(f)

    def run(self): # Método
        while True:
            conectado, imagem = self.camera.read()
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            faceDetectadas = self._classificador.detectMultiScale(imagemCinza, scaleFactor=1.5)

            for (x, y, l, a) in faceDetectadas:
                imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (100, 100))
                cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
                id, confianca = self.reconhecedor.predict(imagemFace)

                if str(id) in self.alunos:
                    print(Aluno(self.alunos[str(id)]))
                    nome = self.alunos[str(id)]
                else:
                    nome = "Desconhecido"

                cv2.putText(imagem, nome, (x, y + a + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))

            cv2.imshow("Face", imagem)
            if cv2.waitKey(1) == ord('q'):
                break

    def __del__(self): # Método destrutor
        self.camera.release()
        cv2.destroyAllWindows()
        print("Objeto ReconhecimentoFacial destruído")

class ClasseAbstrata:
    def metodo_abstrato(self):
        pass

if __name__ == "__main__":
    aluno_data_file = 'BCC-A.json'
    classifier_file = "haarcascade_frontalface_default.xml"
    recognizer_file = 'classificadorLBPH_V1.yml'
    video_source = 'http://192.168.68.104:4747/video'


    reconhecimento = ReconhecimentoFacial(aluno_data_file, classifier_file, recognizer_file, video_source)
    reconhecimento.run()

    print(ReconhecimentoFacial._atributo_protegido)  # Acesso ao atributo protegido
    # print(ReconhecimentoFacial.__atributo_privado)  # Isso causará um erro


    # Não é possível criar uma instância direta de uma classe abstrata em Python
    # classe_abstrata = ClasseAbstrata()
