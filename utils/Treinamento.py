import cv2
import os
import numpy as np

class TreinadorReconhecimentoFacial:
    def __init__(self, data_folder, classifier_filename):
        # Construtor da classe, recebe o diretório de dados e o nome do arquivo do classificador
        self.data_folder = data_folder
        self.classifier_filename = classifier_filename
        self.lbph = cv2.face.LBPHFaceRecognizer_create()  # Instância do classificador LBPH

    def getImagemComId(self):
        # Método para obter imagens e IDs dos rostos a serem treinados
        caminhos = [os.path.join(self.data_folder, f) for f in os.listdir(self.data_folder)]
        faces = []
        ids = []
        for caminhoImagem in caminhos:
            imagemFace = cv2.cvtColor(cv2.imread(caminhoImagem), cv2.COLOR_BGR2GRAY)  # Conversão para tons de cinza
            ra = int(caminhoImagem.split('.')[1])  # Extração do ID do arquivo
            ids.append(ra)
            faces.append(imagemFace)
        return np.array(ids), faces

    def treinarReconhecimentoFacial(self):
        # Método para treinar o reconhecimento facial
        ids, faces = self.getImagemComId()
        print("Treinando....")
        self.lbph.train(faces, ids)  # Treinamento do classificador com os dados
        self.lbph.write(self.classifier_filename)  # Salvando o classificador em um arquivo
        print("Treinamento concluído ...")

if __name__ == "__main__":
    data_folder = 'fotos'  # Diretório contendo as imagens de treinamento
    classifier_filename = 'src\\classificadores\\classificadorLBPH_V1.yml'  # Nome do arquivo do classificador

    treinador = TreinadorReconhecimentoFacial(data_folder, classifier_filename)  # Instância do Treinador
    treinador.treinarReconhecimentoFacial()  # Chamada do método de treinamento