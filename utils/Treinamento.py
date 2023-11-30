import psycopg2
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

con = psycopg2.connect(
	host='localhost', 
	database='postgres', 
	port='5432',
	user='postgres', 
	password='unimar'
)

class TreinadorReconhecimentoFacial:
    def __init__(self):
        # Construtor da classe, recebe o diretório de dados e o nome do arquivo do classificador
        self.lbph = cv2.face.LBPHFaceRecognizer_create()  # Instância do classificador LBPH

    def treinar(self, classifier_filename, id_aula):
        cur = con.cursor()
        sql = """SELECT a.ra, i.imagem FROM aluno a LEFT JOIN imagem i ON i.id_aluno = a.id_aluno WHERE id_aula=%s"""
        cur.execute(sql, (id_aula, ))
        result = cur.fetchall()

        treinamento = {}
        for ra in result:
            if ra[0] not in treinamento:
                treinamento[ra[0]] = {
                    'ra': [],
                    'images': []
                }

        for item in result:
            treinamento[item[0]]['images'].append(np.array(Image.open(BytesIO(item[1]))))
            treinamento[item[0]]['ra'].append(int(item[0]))

        lbph = cv2.face.LBPHFaceRecognizer_create()

        images = np.concatenate([treinamento[ra]['images'] for ra in treinamento])
        labels = np.concatenate([treinamento[ra]['ra'] for ra in treinamento])
        
        lbph.train(images, labels)

        lbph.write(classifier_filename)

    def __del__(self): # Método destrutor
        print("Objeto TreinadorReconhecimentoFacial destruído")

if __name__ == "__main__":
    classifier_filename = 'src\\classificadores\\BCCA.yml'  # Nome do arquivo do classificador

    treinador = TreinadorReconhecimentoFacial()  # Instância do Treinador
    treinador.treinar(classifier_filename, 1)  # Chamada do método de treinamento