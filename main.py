import sys
from loguru import logger
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QMainWindow
from PyQt5 import uic

from pyqt_xbox import QtXBoxInput


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI from the .ui file
        uic.loadUi("window.ui", self)

        # Add your backend logic, signals, etc.
        self.setWindowTitle("PyQt XBox Controller Input Reader")

        self.input = QtXBoxInput(vibrations=False)
        self._connect_window()
        self._connect_inputs()

        self.setFixedSize(self.size())
        self.verticalSlider_rt.setDisabled(True)
        self.verticalSlider_lt.setDisabled(True)
        self.horizontalSlider_right_joy.setDisabled(True)
        self.verticalSlider_right_joy.setDisabled(True)
        self.horizontalSlider_left_joy.setDisabled(True)
        self.verticalSlider_left_joy.setDisabled(True)

        self.button_map = {
            13: self.pushButton_a,
            14: self.pushButton_b,
            15: self.pushButton_x,
            16: self.pushButton_y,
            5: self.pushButton_5,
            6: self.pushButton_6,
            7: self.pushButton_7,
            8: self.pushButton_8,
            10: self.pushButton_rb,
            9: self.pushButton_lb,
            1: self.pushButton_up,
            2: self.pushButton_down,
            3: self.pushButton_left,
            4: self.pushButton_right
        }

        self.axes_mp_ow = {
            'right_trigger': self.verticalSlider_rt,
            'left_trigger': self.verticalSlider_lt,
        }

        self.axes_map = {
            'r_thumb_x': self.horizontalSlider_right_joy,
            'r_thumb_y': self.verticalSlider_right_joy,
            'l_thumb_x': self.horizontalSlider_left_joy,
            'l_thumb_y': self.verticalSlider_left_joy
        }

        self._stop_input()

    def _start_input(self):
        logger.info("Starting input")
        self.label_state.setText("Running")
        self.input.start()

    def _stop_input(self):
        logger.info("Stopping input")
        self.label_state.setText("Not running")
        self.input.stop()

        for button in self.button_map.values():
            self._set_button_state(button, False)

    def _connect_window(self):
        self.pushButton_start.clicked.connect(self._start_input)
        self.pushButton_stop.clicked.connect(self._stop_input)

    def _connect_inputs(self):
        self.input.button_change.connect(self._button_changed)
        self.input.axis_change.connect(self._axis_changed)

    @staticmethod
    def _set_button_state(button: QPushButton, on: bool):
        if on:
            sheet = "QPushButton { background-color: red; }"
        else:
            sheet = "QPushButton { background-color: green; }"
        button.setStyleSheet(sheet)

    @staticmethod
    def _set_axis_position(axis, value: float):
        int_value = int(100 * value + 50)
        if int_value < 1:
            int_value = 1
        elif int_value > 100:
            int_value = 100
        axis.setValue(int_value)

    @staticmethod
    def _set_axis_position_one_way(axis, value: float):
        int_value = int(100 * value)
        if int_value < 1:
            int_value = 1
        elif int_value > 100:
            int_value = 100
        axis.setValue(int_value)

    def _button_changed(self, button: int, on: int):

        if button not in self.button_map:
            logger.warning("Unknown button ({button}) pressed ({on})!")
            return
        self._set_button_state(self.button_map[button], on)

    def _axis_changed(self, axis: str, value: float):

        if axis in self.axes_mp_ow:
            self._set_axis_position_one_way(self.axes_mp_ow[axis], value)
        elif axis in self.axes_map:
            self._set_axis_position(self.axes_map[axis], value)
        else:
            logger.warning("Unknown axis ({axis}) moved ({value})!")


if __name__ == "__main__":
    logger.info("Starting python program...")
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())
