#!/usr/bin/python

from PyQt5 import QtCore,QtWidgets
from functools import partial
import pump_design
import numpy as np
import pump_independent



class pump_ui(object):
    def __init__(self, port = 'COM19'):
        self._control = pump_independent.Control(port)
        self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QWidget()
        self._window.closeEvent = self.shutDown
        self._ui = pump_design.Ui_Form()
        self._ui.setupUi(self._window)


        self._ui.pushButton_run.clicked.connect(self.start)
        self._ui.pushButton_stp.clicked.connect(self.stop)
        self._ui.pushButton_clt.clicked.connect(partial(self.clear, 'T'))
        self._ui.pushButton_status.clicked.connect(self.get_status)
        self._ui.comboBox_dia.currentIndexChanged.connect(self.set_diameter)
        self._ui.comboBox_drt.currentIndexChanged.connect(self.set_direction)

        self._ui.lineEdit_rat.returnPressed.connect(self.set_rate)
        self._ui.lineEdit_vol.returnPressed.connect(self.set_volume)
        # Initialize the UI
        ver = self._control.findPump()
        if (ver == ''):
            print("Cannnot find the pump.")
        self.set_diameter()
        self.set_direction()
        self.reset()

        self._window.show()
        self._app.exec_()
    # ================== Set the syringe pump parameters ====================
    def _status_log_(self):
        '''
        display current status of the pump.
        '''
        pass


    def set_direction(self):
        self.direction = int(self._ui.comboBox_drt.currentIndex())


    def set_rate(self):
        rate = float(self._ui.lineEdit_rat.text())
        units = str(self._ui.comboBox_rat.currentText())
        print(rate, units)
        self._control.setRate(rate, units, self.direction)
    
    def set_diameter(self):
        dia_tx = str(self._ui.comboBox_dia.currentText())
        print(dia_tx)
        self._control.setDiameter(dia_tx)

    def set_volume(self):
        vol_tx = float(self._ui.lineEdit_vol.text())
        self._control.setVolume(vol_tx, self.direction)


    # ================== Operation functions ================================

    def get_status(self):
        status_txt = self._control.getStatus()
        self._ui.TE_status.setPlainText(status_txt)

    def start(self):
        self._control.run(self.direction)

    def stop(self):
        self._control.stop()

    def clear(self, cl_char):
        '''
        clear the vol 
        '''
        if cl_char == 'T':
            pass


    def clear_rat(self):
        '''
        clear the rate
        '''
        pass

    def reset(self):
        self._control.clearTarget(0)
        self._control.clearTarget(1)


def main():
    ui = pump_ui() # generate a UI

if __name__ == '__main__':
    main()
