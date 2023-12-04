import cv2
import threading
import os
from dotenv import load_dotenv

load_dotenv()

VIDEO_SRC = os.getenv('VIDEO_SRC')

class CameraFeed:
    def __init__(self): # Metodo construtor
        try:
            self._camera = cv2.VideoCapture(VIDEO_SRC) # Atributo privado
        except:
            self._camera
        self._lock = threading.Lock()
        
    def __del__(self): # Método destrutor
        self._camera.release()
        cv2.destroyAllWindows()
        print("Objeto Camera destruído")

    def read(self):
        with self._lock:
            con, cap = self._camera.read()

            if not con:
                raise ConnectionError(f"A conexão com a câmera {VIDEO_SRC} foi perdida!")

            img = cv2.resize(cap, (640, 640))

            ret, jpeg = cv2.imencode('.jpg', img)

            return jpeg.tobytes()