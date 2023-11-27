import cv2
import threading

VIDEO_SRC = 0
# VIDEO_SRC = 'http://192.168.137.207:81/stream'

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
            # img = cv2.GaussianBlur(img, (15,15), 0)

            ret, jpeg = cv2.imencode('.jpg', img)

            return jpeg.tobytes()