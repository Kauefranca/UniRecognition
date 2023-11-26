import cv2
import threading
import numpy as np
import time

VIDEO_SRC = 0
# VIDEO_SRC = 'http://192.168.68.102:4747/video'
# VIDEO_SRC = 'http://127.0.0.1:5000/rec'
# 
class Camera:
    def __init__(self): # Metodo construtor
        # time.sleep(5)
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
            # print(cap)

            if not con:
                raise ConnectionError(f"A conexão com a câmera {VIDEO_SRC} foi perdida!")
            
            # nparr = np.frombuffer(cap, np.uint8)
            # cap = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # print(cap)

            return cap