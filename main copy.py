import cv2
import json

class ReconhecimentoFacial:
    def __init__(self, aluno_data_file, classifier_file, recognizer_file, video_source): # Metodo construtor
        self.alunos = self.carregar_alunos(aluno_data_file)
        self._classificador = cv2.CascadeClassifier(classifier_file)
        self._reconhecedor = cv2.face.LBPHFaceRecognizer_create()
        self._reconhecedor.read(recognizer_file)
        self._camera = cv2.VideoCapture(video_source)

    def carregar_alunos(self, aluno_data_file):
        with open(aluno_data_file) as f:
            return json.load(f)

    def run(self):
        while True:
            conectado, imagem = self._camera.read()
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            faceDetectadas = self._classificador.detectMultiScale(imagemCinza, scaleFactor=1.5)

            for (x, y, l, a) in faceDetectadas:
                imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (100, 100))
                cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)

                id, confianca = self._reconhecedor.predict(imagemFace)
                print(confianca)
                print(id)
                if confianca < 80:
                    if str(id) in self.alunos:
                        nome = self.alunos[str(id)]
                else:
                    nome = "Desconhecido"

                cv2.putText(imagem, nome, (x, y + a + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))

            cv2.imshow("Face", imagem)
            if cv2.waitKey(1) == ord('q'):
                break

    def __del__(self): # Método destrutor
        self._camera.release()
        cv2.destroyAllWindows()
        print("Objeto ReconhecimentoFacial destruído")

def capturar_faces(reconhecimento):
    amostra = 1
    numeroAmostras = 25
    curso = input("Digite seu curso/sala Ex. BCC-A: ")
    id = input("Digite seu RA: ")

    while True:
        conectado, imagem = reconhecimento._camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        faceDetectadas = reconhecimento._classificador.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))

        if cv2.waitKey(1) & 0xFF == ord('c'):
            for (x, y, l, a) in faceDetectadas:
                cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
                imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (220, 220))
                cv2.imwrite(f"Fotos/aluno.{str(curso)}.{str(id)}_{str(amostra)}.jpg", imagemFace)
                print("[Foto " + str(amostra) + " capturada com sucesso]")
                amostra += 1

        cv2.imshow("Face", imagem)
        cv2.waitKey(1)
        if  (amostra >= numeroAmostras + 1):
            break

    print("Faces capturadas com sucesso")

if __name__ == "__main__":
    aluno_data_file = 'BCC-A.json'
    classifier_file = "haarcascade_frontalface_default.xml"
    recognizer_file = 'classificadorLBPH_V1.yml'
    video_source = 'http://192.168.68.105:4747/video'

    reconhecimento = ReconhecimentoFacial(aluno_data_file, classifier_file, recognizer_file, video_source)
    reconhecimento.run()

    capturar_faces(reconhecimento)
