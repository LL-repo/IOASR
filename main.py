import sys
import os
import serial
import time
import matplotlib.pyplot as plt
from threading import *
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from gui4 import Ui_MainWindow

global password 
password = ""



def check_password(password):
    '''!@brief Funkcja sprawdzająca podane przez użytkownika hasło.

    Funkcja sprawdzająca podane przez użytkownika hasło w celu zalogowania do systemu.
    Funkcja porównuje wprowadzone hasło z wcześniej zdefiniowanym hasłem dostepowym.

    @param password Hasło wpisane przez użytkownika

    @return password
    '''
    if (password == "admin"):
        return "admin"


class SensorData(Thread):
    '''!@brief Klasa skonfigurowana jako wątek odpowiedzialny za odczyt czujników. 

    Klasa zawiera trzy globalne zmienne temperature, humidity, arduino z czego temperature i humidity
    to tablice przechowujące dane odczytane z czujników.

    '''
    global temperature
    global humidity
    global arduino
    temperature = []
    humidity = []
    arduino = serial.Serial("COM3", 9600)

    def run(self):
        '''!@brief Metoda działająca jako nieskończona pętla.

        Metoda odczytuje stany licznika w nieskończonej pętli, zapisuje je w tablicach
        i za pomocą zmiennej count ogranicza rozmiar zdefiniowanych tablic.

        '''
        count = 0
        while True:
            while (arduino.inWaiting()==0):
                pass      
            arduinoString = arduino.readline() 
            dataTab = arduinoString.decode('UTF-8').split(',')
            temp = int(dataTab[0])
            hum = int(dataTab[1])
            temperature.append(temp)
            humidity.append(hum)
            count = count + 1
            if (count>30):
                temperature.pop(0)
                humidity.pop(0)
            if (temperature[-1] > tempThreshold or humidity[-1] > humThreshold):
                now = datetime.now()
                dt_string = now.strftime('%d/%m/%Y %H:%M:%S')
                name_string = now.strftime("%Y%m%d")
                fileName = os.getcwd()+"\\Data\\"+name_string+".txt"
                f = open(fileName, 'a')
                f.write('Temperatura: ' + str(temperature[-1]) + ' | Wilgotność: ' + str(humidity[-1]) + ' | Data: ' + dt_string + ' | Uwagi: ' + '\n')
                f.close()
                time.sleep(2)

            
class MainWindow():
    '''!@brief Klasa odpowiadająca za działanie GUI.

    Klasa odpowiada za działanie GUI. Posiada dwie globalne zmienne służące do ustalania progów alarmowych
    wprowadzanych przez użytkownika.

    '''
    global tempThreshold
    global humThreshold
    tempThreshold = 30
    humThreshold = 90

    def showCurrentState(self):
        '''!@brief Metoda sprawdzająca aktualne stany czujników'''
        stateMsg = QMessageBox()
        stateMsg.setWindowTitle("Odczyt czujnika")
        stateMsg.setText("Temperatura: " + str(temperature[-1]) + " | " + "Wilgotność: " + str(humidity[-1]))
        stateMsg.setIcon(QMessageBox.Information)
        stateMsg.setStandardButtons(QMessageBox.Ok)
        x = stateMsg.exec_()

    def actualAlarmValue(self):
        '''!@brief Metoda sprawdzająca aktualne progi alarmowe'''
        sensorValMsg = QMessageBox()
        sensorValMsg.setWindowTitle("Aktualne progi alarmowe")
        sensorValMsg.setText("Temperatura: " + str(tempThreshold) + " | " + "Wilgotność: " + str(humThreshold))
        sensorValMsg.setIcon(QMessageBox.Information)
        sensorValMsg.setStandardButtons(QMessageBox.Ok)
        x = sensorValMsg.exec_()

    def setTempAlarmValue(self):
        '''!@brief Metoda ustawiająca próg alarmowy temperatury'''
        tempValue = self.ui.tempEdit.toPlainText()
        global tempThreshold 
        tempThreshold = int(tempValue)
        self.ui.tempEdit.clear()

    def setHumAlarmValue(self):
        '''!@brief Metoda ustawiająca próg alarmowy wilgotności'''
        humValue = self.ui.humEdit.toPlainText()
        global humThreshold
        humThreshold = int(humValue)
        self.ui.humEdit.clear()

    def createPlot(self):
        '''!@brief Metoda generująca wykres temperatury i wilgotności'''
        global temperature
        global humidity
        fig, ax = plt.subplots(2)
        ax[0].plot(temperature)
        ax[0].title.set_text('Temperatura')
        ax[0].set_ylim([20,40])
        ax[1].plot(humidity)
        ax[1].title.set_text('Wilgotność')
        ax[1].set_ylim([40,95])
        plt.show()

    def __init__(self):
        '''!@brief Metoda wywoływana dla nowo utworzonego obiektu.
        
        Metoda zostaje wywołana dla nowo utworzonego obiektu i ustawia GUI.

        '''
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.chart_btn.clicked.connect(self.showPage3)
        self.ui.history_btn.clicked.connect(self.showPage4)
        self.ui.settings_btn.clicked.connect(self.showPage5)
        self.ui.back_btn.clicked.connect(self.showPage2)
        self.ui.back_btn_2.clicked.connect(self.showPage2)
        self.ui.back_btn_3.clicked.connect(self.showPage2)
        self.ui.logout_btn.clicked.connect(self.showPage1)
        self.ui.logout_btn_2.clicked.connect(self.showPage1)
        self.ui.logout_btn_3.clicked.connect(self.showPage1)
        self.ui.logout_btn_4.clicked.connect(self.showPage1)
        self.ui.exit_btn.clicked.connect(self.exitProgram)
        self.ui.exit_btn_2.clicked.connect(self.exitProgram)
        self.ui.exit_btn_3.clicked.connect(self.exitProgram)
        self.ui.exit_btn_4.clicked.connect(self.exitProgram)
        self.ui.exit_btn_5.clicked.connect(self.exitProgram)
        self.ui.login_btn.clicked.connect(self.submitLogin)
        self.ui.browse_btn.clicked.connect(self.openFolder)
        self.ui.sensor_btn.clicked.connect(self.showCurrentState)
        self.ui.aktualne_progi_btn.clicked.connect(self.actualAlarmValue)
        self.ui.confirm_temp_btn.clicked.connect(self.setTempAlarmValue)
        self.ui.confirm_hum_btn.clicked.connect(self.setHumAlarmValue)
        self.ui.chart_sensor.clicked.connect(self.createPlot)

    def showPage1(self):
        '''!@brief Metoda ustawiająca aktualną stronę GUI na stronę logowania'''
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
    def showPage2(self):
        '''!@brief Metoda ustawiająca aktualną stronę GUI na główną'''
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
    def showPage3(self):
        '''!@brief Metoda ustawiająca aktualną stronę GUI na stronę z menu "Wykresy"'''
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
    def showPage4(self):
        '''!@brief Metoda ustawiająca aktualną stronę GUI na stronę z menu "Historia"'''
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_4)
    def showPage5(self):
        '''!@brief Metoda ustawiająca aktualną stronę GUI na stronę z menu "Ustawienia"'''
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_5)
    def exitProgram(self):
        '''!@brief Metoda zamykająca program'''
        sys.exit(0)

    def show(self):
        '''!@brief Metoda wyświetlająca GUI'''
        self.main_win.show()

    def submitLogin(self):
        '''!@brief Metoda umożliwiająca zalogowanie do systemu'''
        login = "admin"
        global password
        password = self.ui.haslo.text()
        if self.ui.login.text() == login and self.ui.haslo.text() == check_password(password):
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
            self.ui.login.clear()
            self.ui.haslo.clear()

    def openFolder(self):
        '''!@brief Metoda otwierająca folder z zapisanymi plikami alarmów'''
        path = os.getcwd()+"\Data"
        os.startfile(path)

class threadGUI(Thread):
    '''!@brief Klasa skonfigurowana jako wątek odpowiedzialny za GUI.'''
    def run(self):
        '''!@brief Metoda uruchamiająca GUI'''
        if __name__ == '__main__':
            app = QApplication(sys.argv)
            main_win = MainWindow()
            main_win.show()
            sys.exit(app.exec_())


t1 = threadGUI()
t2 = SensorData()
t1.start()
t2.start()



    





