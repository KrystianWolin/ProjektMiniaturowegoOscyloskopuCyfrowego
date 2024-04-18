from PyQt5 import QtCore, QtGui, QtWidgets

from windowCreator import Ui_MainWindow
from connectionByUSB import UART

import time
import numpy as np
from threading import *
from enum import Enum
from statistics import mean


class TimeBase(Enum):
    T100S = 1
    T050S = 2
    T020S = 3
    T010S = 4
    T005S = 5
    T002S = 6
    T001S = 7

    T100M = 8
    T050M = 9
    T020M = 10
    T010M = 11
    T005M = 12
    T002M = 13
    T001M = 14


class VoltBase(Enum):
    U100V = 1
    U050V = 2
    U020V = 3
    U010V = 4
    U005V = 5
    U002V = 6
    U001V = 7

    U500M = 8
    U200M = 9
    U100M = 10
    U050M = 11
    U020M = 12
    U010M = 13
    U005M = 14
    U002M = 15
    U001M = 16


class Factor(Enum):
    X001 = 1
    X010 = 10
    X100 = 100


class Engine(QtCore.QObject):
    bufforX = [0]
    bufforY = [128.0]
    timeBase = TimeBase.T100S
    voltBase = VoltBase.U005V
    continousWork = True
    stopTime = 0
    sampleTime = 0
    factor = Factor.X001

    cx1vInEdit = False
    cx1v = 0
    cx2vInEdit = False
    cx2v = 0
    cy1vInEdit = False
    cy1v = 0
    cy2vInEdit = False
    cy2v = 0
    plotCursors = False

    def __init__(self):
        super(Engine, self).__init__()
        # gui
        self.app = QtWidgets.QApplication([])
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(engine=self)

        self.ui.dialHTB.setValue(4)
        self.ui.dialVVO.setValue(6)
        self.ui.pushButtonStartStop.setStyleSheet("color: rgb(0, 170, 0);")
        self.ui.pushButtonStartStop.clicked.connect(self.startStop)
        self.ui.pushButtonClear.clicked.connect(self.clearBuffor)
        self.ui.dialVVO.valueChanged.connect(self.setVB)
        self.ui.dialHTB.valueChanged.connect(self.setTB)

        self.ui.Oscreen.scene().sigMouseClicked.connect(self.mouseClicked)
        self.ui.pushButtonCX1.clicked.connect(self.CX1)
        self.ui.pushButtonCX2.clicked.connect(self.CX2)
        self.ui.pushButtonCY1.clicked.connect(self.CY1)
        self.ui.pushButtonCY2.clicked.connect(self.CY2)
        self.ui.pushButtonCursorsOnOff.clicked.connect(self.plotCursorsOnOff)

        self.ui.pushButtonX001.clicked.connect(self.factorerX1)
        self.ui.pushButtonX010.clicked.connect(self.factorerX10)
        self.ui.pushButtonX100.clicked.connect(self.factorerX100)

        self.ui.horizontalScrollBar.valueChanged.connect(self.hScrollBar)
        self.ui.verticalScrollBar.valueChanged.connect(self.vScrollBar)

        # uart
        self.uart = UART()

        # timer
        self.timerRead = QtCore.QTimer()
        self.timerRead.setInterval(1)  # 1ms -> 1000Hz
        self.timerRead.timeout.connect(self.read)
        self.timerRead.start()

        self.timerView = QtCore.QTimer()
        self.timerView.setInterval(10)  # 10ms -> 100Hz
        self.timerView.timeout.connect(self.view)
        self.timerView.start()

        # on app exit
        # self.app.aboutToQuit(self.on_app_exit)

    def run_app(self):
        self.MainWindow.show()
        return self.app.exec_()

    def factorerX1(self):
        self.factor = Factor.X001
        self.ui.pushButtonX001.setStyleSheet("color: rgb(0, 170, 0);")
        self.ui.pushButtonX010.setStyleSheet("color: rgb(255, 255, 255);")
        self.ui.pushButtonX100.setStyleSheet("color: rgb(255, 255, 255);")

    def factorerX10(self):
        self.factor = Factor.X010
        self.ui.pushButtonX001.setStyleSheet("color: rgb(255, 255, 255);")
        self.ui.pushButtonX010.setStyleSheet("color: rgb(0, 170, 0);")
        self.ui.pushButtonX100.setStyleSheet("color: rgb(255, 255, 255);")

    def factorerX100(self):
        self.factor = Factor.X100
        self.ui.pushButtonX001.setStyleSheet("color: rgb(255, 255, 255);")
        self.ui.pushButtonX010.setStyleSheet("color: rgb(255, 255, 255);")
        self.ui.pushButtonX100.setStyleSheet("color: rgb(0, 170, 0);")

    def setVB(self, number):
        if number == 1:
            self.voltBase = VoltBase.U100V
        elif number == 2:
            self.voltBase = VoltBase.U050V
        elif number == 3:
            self.voltBase = VoltBase.U020V
        elif number == 4:
            self.voltBase = VoltBase.U010V
        elif number == 5:
            self.voltBase = VoltBase.U005V
        elif number == 6:
            self.voltBase = VoltBase.U002V
        elif number == 7:
            self.voltBase = VoltBase.U001V
        elif number == 8:
            self.voltBase = VoltBase.U500M
        elif number == 9:
            self.voltBase = VoltBase.U200M
        elif number == 10:
            self.voltBase = VoltBase.U100M
        elif number == 11:
            self.voltBase = VoltBase.U050M
        elif number == 12:
            self.voltBase = VoltBase.U020M
        elif number == 13:
            self.voltBase = VoltBase.U010M
        elif number == 14:
            self.voltBase = VoltBase.U005M
        elif number == 15:
            self.voltBase = VoltBase.U002M
        elif number == 16:
            self.voltBase = VoltBase.U001M

        start = 0
        start = int(self.voltBase.name[1]) * 100 + int(self.voltBase.name[2]) * 10 + int(self.voltBase.name[3])
        if self.voltBase.name[4] == "V":
            start = start * 1000
        else:
            start = start

        now = -int(self.ui.verticalScrollBar.value())
        self.ui.Oscreen.setYRange((-start * self.factor.value) + now, (start * self.factor.value) + now)

        print(number)

    def getVB(self):
        return self.timeBase.value

    def setTB(self, number):
        if number == 1:
            self.timeBase = TimeBase.T100S
        elif number == 2:
            self.timeBase = TimeBase.T050S
        elif number == 3:
            self.timeBase = TimeBase.T020S
        elif number == 4:
            self.timeBase = TimeBase.T010S
        elif number == 5:
            self.timeBase = TimeBase.T005S
        elif number == 6:
            self.timeBase = TimeBase.T002S
        elif number == 7:
            self.timeBase = TimeBase.T001S
        elif number == 8:
            self.timeBase = TimeBase.T100M
        elif number == 9:
            self.timeBase = TimeBase.T050M
        elif number == 10:
            self.timeBase = TimeBase.T020M
        elif number == 11:
            self.timeBase = TimeBase.T010M
        elif number == 12:
            self.timeBase = TimeBase.T005M
        elif number == 13:
            self.timeBase = TimeBase.T002M
        elif number == 14:
            self.timeBase = TimeBase.T001M

        now = int(self.ui.horizontalScrollBar.value())  # self.stopTime
        # print("now"+str(now))
        start = 0
        start = int(self.timeBase.name[1]) * 100 + int(self.timeBase.name[2]) * 10 + int(self.timeBase.name[3])
        if self.timeBase.name[4] == "S":
            start = start * 1000000
        elif self.timeBase.name[4] == "M":
            start = start * 1000
        else:
            start = start

        self.ui.Oscreen.setXRange(now - start, now)

        print(number)

    def getTB(self):
        return self.timeBase.value

    def startStop(self):
        if self.continousWork == True:
            self.ui.pushButtonStartStop.setStyleSheet("color: rgb(255, 255, 255);")
            self.continousWork = False
            bX = self.bufforX
            bY = self.bufforY
            self.ui.Oscreen.update_ch(bX, bY)
            self.stopTime = bX[len(bX) - 1]
            self.ui.Oscreen.setXRange(0, self.stopTime)

            # obliczanie wartosci max i min napiecia
            maxY = max(bY)
            # print(maxY)
            self.ui.labelMaxV.setText(str(maxY))
            minY = min(bY)
            # print(minY)
            self.ui.labelMinV.setText(str(minY))

            # obliczanie wartosci sredniej
            avgY = int(mean(bY))
            # print(avgY)
            self.ui.labelAvgV.setText(str(avgY))

            # obliczanie wartosci PP
            ppY = maxY - minY
            self.ui.labelPPV.setText(str(ppY))

            # obliczanie czestotliwosci sygnalu
            lastTime = len(bX)
            number = 0
            for i in range(0, lastTime - 2, 1):
                if bY[i] <= avgY and bY[i + 1] > avgY:
                    number += 1
                elif bY[i] >= avgY and bY[i + 1] < avgY:
                    number += 1
            freq = round((number / 2) / (bX[len(bX) - 1] / 1000000), 2)
            self.ui.labelFrequency.setText(str(freq))

            # obliczanie okresu
            period = round(1000 / freq, 2)
            self.ui.labelPeriod.setText(str(period))

        else:
            self.ui.pushButtonStartStop.setStyleSheet("color: rgb(0, 170, 0);")
            self.continousWork = True

    def clearBuffor(self):
        self.bufforX = [0]
        self.bufforY = [0.0]

    def mouseClicked(self, event):
        # Sprawdzamy, czy kliknięcie myszy miało miejsce na wykresie
        if self.ui.Oscreen.sceneBoundingRect().contains(event.scenePos()):
            if self.cx1vInEdit == True:
                # Pobieramy współrzędne punktu na wykresie
                pos = self.ui.Oscreen.plotItem.vb.mapSceneToView(event.scenePos())
                x = pos.x()
                # print(f"Kliknięto na pozycji: x={x}, y={y}")
                self.cx1v = x
                if x < 10000:
                    self.ui.labelCX1V.setText(str(round(x, 2)) + "us")
                elif x < 10000000:
                    self.ui.labelCX1V.setText(str(round(x / 1000, 2)) + "ms")
                else:
                    self.ui.labelCX1V.setText(str(round(x / 1000000, 2)) + "s")

                delta = abs(self.cx1v - self.cx2v)
                if delta < 10000:
                    self.ui.labelDeltaX.setText(str(round(delta, 2)) + "us")
                elif delta < 10000000:
                    self.ui.labelDeltaX.setText(str(round(delta / 1000, 2)) + "ms")
                else:
                    self.ui.labelDeltaX.setText(str(round(delta / 1000000, 2)) + "s")

                if self.plotCursors == True:
                    self.ui.Oscreen.update_cx1([self.cx1v, self.cx1v], [-330000, 400000])

            if self.cx2vInEdit == True:
                pos = self.ui.Oscreen.plotItem.vb.mapSceneToView(event.scenePos())
                x = pos.x()
                self.cx2v = x
                if x < 10000:
                    self.ui.labelCX2V.setText(str(round(x, 2)) + "us")
                elif x < 10000000:
                    self.ui.labelCX2V.setText(str(round(x / 1000, 2)) + "ms")
                else:
                    self.ui.labelCX2V.setText(str(round(x / 1000000, 2)) + "s")

                delta = abs(self.cx1v - self.cx2v)
                if delta < 10000:
                    self.ui.labelDeltaX.setText(str(round(delta, 2)) + "us")
                elif delta < 10000000:
                    self.ui.labelDeltaX.setText(str(round(delta / 1000, 2)) + "ms")
                else:
                    self.ui.labelDeltaX.setText(str(round(delta / 1000000, 2)) + "s")

                if self.plotCursors == True:
                    self.ui.Oscreen.update_cx2([self.cx2v, self.cx2v], [-330000, 400000])

            if self.cy1vInEdit == True:
                pos = self.ui.Oscreen.plotItem.vb.mapSceneToView(event.scenePos())
                y = pos.y()
                self.cy1v = y
                if y < 10000:
                    self.ui.labelCY1V.setText(str(round(y, 2)) + "mV")
                else:
                    self.ui.labelCY1V.setText(str(round(y / 1000, 2)) + "V")

                delta = abs(self.cy1v - self.cy2v)
                if delta < 10000:
                    self.ui.labelDeltaY.setText(str(round(delta, 2)) + "mV")
                else:
                    self.ui.labelDeltaY.setText(str(round(delta / 1000, 2)) + "V")

                if self.plotCursors == True:
                    self.ui.Oscreen.update_cy1([-100, 6000000000], [self.cy1v, self.cy1v])

            if self.cy2vInEdit == True:
                pos = self.ui.Oscreen.plotItem.vb.mapSceneToView(event.scenePos())
                y = pos.y()
                self.cy2v = y
                if y < 10000:
                    self.ui.labelCY2V.setText(str(round(y, 2)) + "mV")
                else:
                    self.ui.labelCY2V.setText(str(round(y / 1000, 2)) + "V")

                delta = abs(self.cy1v - self.cy2v)
                if delta < 10000:
                    self.ui.labelDeltaY.setText(str(round(delta, 2)) + "mV")
                else:
                    self.ui.labelDeltaY.setText(str(round(delta / 1000, 2)) + "V")

                if self.plotCursors == True:
                    self.ui.Oscreen.update_cy2([-100, 6000000000], [self.cy2v, self.cy2v])

    def CX1(self):
        if self.cx1vInEdit == True:
            self.ui.pushButtonCX1.setStyleSheet("color: rgb(255, 255, 255);")
            self.cx1vInEdit = False
        else:
            self.ui.pushButtonCX1.setStyleSheet("color: rgb(0, 170, 0);")
            self.cx1vInEdit = True

    def CX2(self):
        if self.cx2vInEdit == True:
            self.ui.pushButtonCX2.setStyleSheet("color: rgb(255, 255, 255);")
            self.cx2vInEdit = False
        else:
            self.ui.pushButtonCX2.setStyleSheet("color: rgb(0, 170, 0);")
            self.cx2vInEdit = True

    def CY1(self):
        if self.cy1vInEdit == True:
            self.ui.pushButtonCY1.setStyleSheet("color: rgb(255, 255, 255);")
            self.cy1vInEdit = False
        else:
            self.ui.pushButtonCY1.setStyleSheet("color: rgb(0, 170, 0);")
            self.cy1vInEdit = True

    def CY2(self):
        if self.cy2vInEdit == True:
            self.ui.pushButtonCY2.setStyleSheet("color: rgb(255, 255, 255);")
            self.cy2vInEdit = False
        else:
            self.ui.pushButtonCY2.setStyleSheet("color: rgb(0, 170, 0);")
            self.cy2vInEdit = True

    def plotCursorsOnOff(self):
        if self.plotCursors == True:
            self.ui.pushButtonCursorsOnOff.setStyleSheet("color: rgb(255, 255, 255);")
            self.plotCursors = False
            self.cx1vInEdit = False
            self.cx2vInEdit = False
            self.cy1vInEdit = False
            self.cy2vInEdit = False
            # clear cursors
            self.ui.Oscreen.update_cx1([0, 0], [0, 0])
            self.ui.Oscreen.update_cx2([0, 0], [0, 0])
            self.ui.Oscreen.update_cy1([0, 0], [0, 0])
            self.ui.Oscreen.update_cy2([0, 0], [0, 0])
        else:
            self.ui.pushButtonCursorsOnOff.setStyleSheet("color: rgb(0, 170, 0);")
            self.plotCursors = True
            # drow all cursors
            self.ui.Oscreen.update_cx1([self.cx1v, self.cx1v], [-330000, 400000])
            self.ui.Oscreen.update_cx2([self.cx2v, self.cx2v], [-330000, 400000])
            self.ui.Oscreen.update_cy1([-100, 6000000000], [self.cy1v, self.cy1v])
            self.ui.Oscreen.update_cy2([-100, 6000000000], [self.cy2v, self.cy2v])

    def hScrollBar(self):
        n = int(self.ui.horizontalScrollBar.value())
        ns = self.set_Time(n)
        self.ui.Oscreen.setXRange(ns, n)

    def vScrollBar(self):
        self.set_Volts(-int(self.ui.verticalScrollBar.value()))

    def set_Time(self, now):  # timebase
        start = 0
        start = int(self.timeBase.name[1]) * 100 + int(self.timeBase.name[2]) * 10 + int(self.timeBase.name[3])
        if self.timeBase.name[4] == "S":
            start = start * 1000000
        elif self.timeBase.name[4] == "M":
            start = start * 1000
        else:
            start = start

        # print(now - start, now)
        if self.continousWork:
            self.ui.Oscreen.setXRange(now - start, now)

        return now - start

    def set_Volts(self, now):  # voltbase
        start = 0
        start = int(self.voltBase.name[1]) * 100 + int(self.voltBase.name[2]) * 10 + int(self.voltBase.name[3])
        if self.voltBase.name[4] == "V":
            start = start * 1000
        else:
            start = start

        self.ui.Oscreen.setYRange((-start * self.factor.value) + now, (start * self.factor.value) + now)

    def filtrOfData(self, value):
        # print(value)
        try:
            result = float(value)
        except ValueError:
            result = self.bufforY[len(self.bufforY) - 1]

        if len(self.bufforY) > 1 and result >= 27 * self.bufforY[len(self.bufforY) - 1]:
            result = self.bufforY[len(self.bufforY) - 1]

        return result

    def read(self):
        # odczytaj dane
        # dodaj do bufforY

        readData = self.uart.readU()  # 101 -> [0-100]
        # print(readData)

        if len(readData) > 0:
            sampleNumber = len(readData) - 1  # 101-1=100
            try:
                self.sampleTime = int(readData[0])  # 100
            except ValueError:
                self.sampleTime = self.sampleTime

            for i in range(0, sampleNumber, 1):  # <0 - 100)
                self.bufforY.append(self.filtrOfData(readData[1 + i]) * self.factor.value)  # 0+1 - 99+1 -> 1 - 100

    def view(self):
        # generuj bufforX
        # ustaw zakres osi x jesli tryb ciagly
        # wyswietl dane wg potrzeby

        if self.bufforX[len(self.bufforX) - 1] >= 500000000:
            self.clearBuffor()

        sampleDiff = len(self.bufforY) - len(self.bufforX)
        lastTime = self.bufforX[len(self.bufforX) - 1]

        for i in range(0, sampleDiff, 1):
            self.bufforX.append(lastTime + self.sampleTime * (i + 1))
            # print(lastTime + self.sampleTime * (i+1))

        nowT = self.bufforX[len(self.bufforX) - 1]

        start = self.set_Time(nowT)
        sampleToView = int(len(self.bufforX) - 1 - (nowT - start) / self.sampleTime)
        if sampleToView < 0:
            sampleToView = 0

        # print("sampleToView"+str(sampleToView))

        if self.continousWork:
            self.ui.horizontalScrollBar.setMaximum(int(nowT))

            podzial = int(self.timeBase.name[1]) * 100 + int(self.timeBase.name[2]) * 10 + int(self.timeBase.name[3])
            if self.timeBase.name[4] == "S":
                podzial = podzial * 1000000
            elif self.timeBase.name[4] == "M":
                podzial = podzial * 1000
            else:
                podzial = podzial

            if podzial == 1000:
                self.ui.Oscreen.update_ch(self.bufforX[sampleToView::1], self.bufforY[sampleToView::1])
            elif podzial <= 10000:
                self.ui.Oscreen.update_ch(self.bufforX[sampleToView::2], self.bufforY[sampleToView::2])
            elif podzial <= 100000:
                self.ui.Oscreen.update_ch(self.bufforX[sampleToView::5], self.bufforY[sampleToView::5])
            elif podzial <= 1000000:
                self.ui.Oscreen.update_ch(self.bufforX[sampleToView::20], self.bufforY[sampleToView::20])
            elif podzial <= 10000000:
                self.ui.Oscreen.update_ch(self.bufforX[sampleToView::50], self.bufforY[sampleToView::50])
            elif podzial <= 100000000:
                self.ui.Oscreen.update_ch(self.bufforX[sampleToView::200], self.bufforY[sampleToView::200])

                # self.ui.Oscreen.update_cursor([0,1],[1,10])

    def on_app_exit(self):
        print("exiting")
        # self.disconnect_device()
        self.app.quit()

