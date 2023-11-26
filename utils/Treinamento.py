import cv2
import os
import numpy as np

class TreinadorReconhecimentoFacial:
    def __init__(self, classifier_filename):
        # Construtor da classe, recebe o diretório de dados e o nome do arquivo do classificador
        self.classifier_filename = classifier_filename
        self.lbph = cv2.face.LBPHFaceRecognizer_create()  # Instância do classificador LBPH

    def treinar(self):
        ras = os.listdir(os.path.join('fotos'))
        treinamento = {}

        for ra in ras:
            if ra not in treinamento:
                treinamento[ra] = {
                    'ra': [],
                    'images': []
                }

            for item in os.listdir(os.path.join('fotos', ra)):
                treinamento[ra]['images'].append(cv2.cvtColor(cv2.imread(os.path.join('fotos', ra, item)),cv2.COLOR_BGR2GRAY))
                treinamento[ra]['ra'].append(int(ra))

        lbph = cv2.face.LBPHFaceRecognizer_create()

        images = np.concatenate([treinamento[ra]['images'] for ra in treinamento])
        labels = np.concatenate([treinamento[ra]['ra'] for ra in treinamento])
        
        lbph.train(images, labels)

        lbph.write(self.classifier_filename)

    def __del__(self): # Método destrutor
        print("Objeto TreinadorReconhecimentoFacial destruído")

if __name__ == "__main__":
    classifier_filename = 'src\\classificadores\\BCCA.yml'  # Nome do arquivo do classificador

    treinador = TreinadorReconhecimentoFacial(classifier_filename)  # Instância do Treinador
    treinador.treinar()  # Chamada do método de treinamento