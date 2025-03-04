import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SignalGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sampling_rate = 1000
        self.duration = 1.0
        self.t = np.linspace(0, self.duration, int(self.sampling_rate * self.duration), endpoint=False) 

        self.amplitude_inputs = [QLineEdit("1.0"), QLineEdit("0.5"), QLineEdit("0.3")]
        self.frequency_inputs = [QLineEdit("5"), QLineEdit("10"), QLineEdit("25")]
        self.phase_inputs = [QLineEdit("0"), QLineEdit("0.785"), QLineEdit("1.57")]
        self.noise_level_input = QLineEdit("0.1")

        self.update_button = QPushButton("Обновить график")
        self.update_button.clicked.connect(self.update_plot)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Амплитуды:"))
        for inp in self.amplitude_inputs:
            input_layout.addWidget(inp)
        input_layout.addWidget(QLabel("Частоты:"))
        for inp in self.frequency_inputs:
            input_layout.addWidget(inp)
        input_layout.addWidget(QLabel("Фазы:"))
        for inp in self.phase_inputs:
            input_layout.addWidget(inp)
        input_layout.addWidget(QLabel("Уровень шума:"))
        input_layout.addWidget(self.noise_level_input)
        input_layout.addWidget(self.update_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)
        self.setWindowTitle("Генератор сигналов")
        self.update_plot() 

    def update_plot(self):
        amplitudes = [float(inp.text()) for inp in self.amplitude_inputs]
        frequencies = [float(inp.text()) for inp in self.frequency_inputs]
        phases = [float(inp.text()) for inp in self.phase_inputs]
        noise_level = float(self.noise_level_input.text())

        signal = np.zeros_like(self.t)
        for A, f, phi in zip(amplitudes, frequencies, phases):
            signal += A * np.sin(2 * np.pi * f * self.t + phi)

        noise = noise_level * np.random.normal(size=len(self.t))
        noisy_signal = signal + noise

        self.ax.clear()
        self.ax.plot(self.t, signal, label="Детерминированный сигнал")
        self.ax.plot(self.t, noisy_signal, label="Сигнал с шумом", alpha=0.7)
        self.ax.set_title("Полигармонический сигнал")
        self.ax.set_xlabel("Время (сек)")
        self.ax.set_ylabel("Амплитуда")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalGeneratorApp()
    window.show()
    sys.exit(app.exec_())