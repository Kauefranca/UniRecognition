import cv2
import threading

VIDEO_SRC = 'http://192.168.68.102:4747/video'

class Camera:
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

            ret, jpeg = cv2.imencode('.jpg', cap)

            return jpeg.tobytes()