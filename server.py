import zlib
import socket
import cv2
import numpy as np
# import win32api
# import win32con
import math
# Monitors resolution
# WIDTH = win32api.GetSystemMetrics(0)
# HEIGHT = win32api.GetSystemMetrics(1)

# 1920x1080 FOR MY SCREENs
WIDTH = 1920
HEIGHT = 1080
# Softwares resolution
SWIDTH = 960
SHEIGHT = 540

class servercontrol:
    def __init__(self, ip: str = "0.0.0.0", port: int = 443):
        self.ip = ip
        self.port = port
        self.socket = None
        self.connect()

    def recvdata(self, buffer: int=4096, data: bytes=b''):
        while True:
            part = self.socket.recv(buffer)
            data += part
            if len(part) < buffer:
                break
        return data

    def showcords(self, event, x, y, flags, params) -> int:
        xRatio = WIDTH / SWIDTH
        yRatio = HEIGHT / SHEIGHT
        x = str(math.ceil(x*xRatio))
        y = str(math.ceil(y*yRatio))
        self.socket.send(bytes(x + y, "utf-8"))
        # win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_HAND))
        return event

    def showscreen(self, img) -> None:
        ''' Decompresses and displays on screen '''
        decompress = zlib.decompress(img)
        nparr = np.frombuffer(decompress, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, (SWIDTH, SHEIGHT))
        cv2.imshow('frame', frame)
        cv2.setMouseCallback("frame", self.showcords)
        cv2.waitKey(1)

    def connect(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(1)
        self.socket, _ = sock.accept()
        print("CLient connected!")
        self.socket.send(b"Welcome")
        while True:
            data = self.recvdata()
            self.showscreen(data)


if __name__ == '__main__':
    servercontrol()