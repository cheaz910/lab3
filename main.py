import sys, random, math, time, threading, serial
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore

MAX_DISTANCE = 80

def thread(my_func):
    """
    Запускает функцию в отдельном потоке
    """
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper
 
@thread
def processing(signal):
    """
    Получаю координаты по Serial и передаю через сигналы основному потоку
    """
    ser = serial.Serial('COM5', 115200)
    while True:
        data = ser.readline().decode()
        deg, distance = map(lambda x: math.floor(float(x)), data.split())
        distance = distance * 200 / 80
        if distance > 200:
            distance = 200
        x = math.cos(deg * math.pi / 180) * distance + 210
        y = math.sin(deg * math.pi / 180) * distance + 210
        signal.emit([deg, x, y])
    return
    
    deg = 0
    sign = 1
    while True:
        r = random.randint(0, 201)
        deg += 1 * sign
        is_point = random.randint(0, 100)
        if is_point > 2:
            print(deg, 'no')
            signal.emit([deg, '-', '-'])
        else:
            x = math.cos(deg * math.pi / 180) * r + 210
            y = math.sin(deg * math.pi / 180) * r + 210
            print('sended:', deg, x, y)
            signal.emit([deg, x, y])  # Посылаем сигнал в котором передаём полученные данные
        if deg == 360:
            sign = -1
        if deg == 0:
            sign = 1
        time.sleep(0.05)


class Example(QWidget):
    my_signal = QtCore.pyqtSignal(list, name='my_signal')
    
    def __init__(self):
        super().__init__()

        self.my_signal.connect(self.mySignalHandler, QtCore.Qt.QueuedConnection)
        self.initUI()

 
    def mySignalHandler(self, data):  # Вызывается для обработки сигнала
        self.points[data[0]] = [data[1], data[2]]
        self.update()
        


    def initUI(self):

        self.setGeometry(300, 200, 420, 420)
        self.setWindowTitle('Points')
        self.points = {} # ключ - угол, значение - 
        self.show()
        self.deg = 0
        self.sign = 1
        processing(self.my_signal)


    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
 
 
        qp.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        qp.drawEllipse(10, 10, 400, 400)
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.drawEllipse(210, 210, 6, 6)
        x = math.cos(self.deg * math.pi / 180) * 200 + 210
        y = math.sin(self.deg * math.pi / 180) * 200 + 210
        qp.drawLine(213, 213, x, y)
        for point in self.points:
            if self.points[point][0] == '-':
                continue
            qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
            qp.drawPoint(self.points[point][0], self.points[point][1])
        qp.end()
        self.deg += 1 * self.sign
        if self.deg == 180:
            self.sign = -1
        if self.deg == 0:
            self.sign = 1
        return
 
 
        qp.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        qp.drawEllipse(10, 10, 400, 400)
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.drawEllipse(210, 210, 6, 6)
        
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        #qp.drawLine(213,213,400,400)
        center = 210
        radius = 200
        for i in range(10,411):
            #print(radius, i, 'gg')
            y = math.sqrt(radius**2 - (i - 210)**2) + 210
            #qp.drawLine(213,213,i, y)
            #print(y)
        qp.end()


    def drawPoints(self, qp):

        qp.setPen(Qt.red)
        size = self.size()

        #for i in range(size.width()):
        #    qp.drawPoint(i, i)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())