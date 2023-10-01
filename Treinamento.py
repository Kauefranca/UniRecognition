import cv2
import os
import numpy as np

lbph = cv2.face.LBPHFaceRecognizer_create()

def getImagemComId():
    caminhos = [os.path.join('fotos', f) for f in os.listdir('fotos')]
    faces = []
    ids = []
    for caminhosImagem in caminhos:
        imagemFace = cv2.cvtColor(cv2.imread(caminhosImagem), cv2.COLOR_BGR2GRAY)
        ra = int(caminhosImagem.split('.')[2][0])
        # turma = str(caminhosImagem.split('.')[1][0])
        ids.append(ra)
        faces.append(imagemFace)
    return np.array(ids), faces

ids, faces = getImagemComId()

print("Treinando....")

lbph.train(faces, ids)
lbph.write('classificadorLBPH_V1.yml')

print("Treinamento concluído ...")