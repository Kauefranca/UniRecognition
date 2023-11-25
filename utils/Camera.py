import cv2

VIDEO_SRC = 0

class Camera:
    def __init__(self): # Metodo construtor
        self._camera = cv2.VideoCapture(VIDEO_SRC) # Atributo privado
    
    def __del__(self): # Método destrutor
        self._camera.release()
        cv2.destroyAllWindows()
        print("Objeto Camera destruído")

    def read(self):
        con, cap = self._camera.read()

        if not con:
            raise ConnectionError(f"A conexão com a câmera {VIDEO_SRC} foi perdida!")

        return cap