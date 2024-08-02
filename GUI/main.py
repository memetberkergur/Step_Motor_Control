import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QDesktopWidget, QMessageBox
import serial
import serial.tools.list_ports
import time

class MotorControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ser = None
        self.total_distance = 0  # Toplam mm mesafe
        self.step_distance = 0.01  # Her adım için mesafe (mm) - Burada adım başına mm değerini ayarlayın
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Stepper Motor Control')
        self.resize(400, 400)  # Arayüzün boyutlarını statik olarak ayarlayın
        self.center()  # Arayüzü ekranın ortasına yerleştirin
        
        layout = QVBoxLayout()

        self.portLabel = QLabel('USB Port:')
        self.portComboBox = QComboBox()
        self.updatePorts()
        layout.addWidget(self.portLabel)
        layout.addWidget(self.portComboBox)

        self.baudRateLabel = QLabel('Baud Rate:')
        self.baudRateComboBox = QComboBox()
        self.baudRateComboBox.addItems([
            '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', 
            '28800', '38400', '57600', '76800', '115200', '230400', '250000'
        ])
        self.baudRateComboBox.setCurrentText('115200')
        layout.addWidget(self.baudRateLabel)
        layout.addWidget(self.baudRateComboBox)

        self.refreshButton = QPushButton('Refresh Ports')
        self.refreshButton.clicked.connect(self.updatePorts)
        layout.addWidget(self.refreshButton)

        self.connectButton = QPushButton('Connect')
        self.connectButton.clicked.connect(self.connectSerial)
        layout.addWidget(self.connectButton)

        self.speedLabel = QLabel('Speed:')
        self.speedInput = QLineEdit()
        self.speedInput.setText('1000')
        layout.addWidget(self.speedLabel)
        layout.addWidget(self.speedInput)

        self.accelerationLabel = QLabel('Acceleration:')
        self.accelerationInput = QLineEdit()
        self.accelerationInput.setText('500')
        layout.addWidget(self.accelerationLabel)
        layout.addWidget(self.accelerationInput)

        self.stepsLabel = QLabel('Steps:')
        self.stepsInput = QLineEdit()
        self.stepsInput.setText('1440')
        layout.addWidget(self.stepsLabel)
        layout.addWidget(self.stepsInput)

        self.moveLabel = QLabel('Move (mm):')
        self.moveInput = QLineEdit()
        self.moveInput.setText('1')
        layout.addWidget(self.moveLabel)
        layout.addWidget(self.moveInput)

        self.startButton = QPushButton('START')
        self.startButton.clicked.connect(self.sendStartCommand)
        layout.addWidget(self.startButton)

        self.statusLabel = QLabel('Status: Idle')
        layout.addWidget(self.statusLabel)

        # Total Distance / Absolute Position Label
        self.positionLabel = QLabel(f'Absolute Position: {self.total_distance:.2f} mm')
        layout.addWidget(self.positionLabel)

        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def updatePorts(self):
        self.portComboBox.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.portComboBox.addItem(port.device)

    def connectSerial(self):
        port = self.portComboBox.currentText()
        baud_rate = self.baudRateComboBox.currentText()
        try:
            self.ser = serial.Serial(port, baud_rate, timeout=1)  # Seri portu ayarlayın
            time.sleep(2)  # Seri portun açılması için biraz bekleyin
            self.statusLabel.setText("Status: Connected")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to serial port: {e}")
            self.statusLabel.setText("Status: Not Connected")

    def sendCommand(self, command):
        if self.ser is not None:
            self.ser.write((command + '\n').encode())
            time.sleep(0.1)  # Komutların gönderilmesi arasında biraz bekleyin
            response = self.ser.readline().decode().strip()
            self.statusLabel.setText(f"Status: {response}")
        else:
            QMessageBox.critical(self, "Error", "Serial port not connected.")
            self.statusLabel.setText("Status: Not Connected")

    def sendStartCommand(self):
        speed = self.speedInput.text()
        if speed:
            self.sendCommand(f"SPD {speed}")

        acceleration = self.accelerationInput.text()
        if acceleration:
            self.sendCommand(f"ACC {acceleration}")

        steps = self.stepsInput.text()
        if steps:
            self.sendCommand(f"STEPS {steps}")

        move = self.moveInput.text()
        if move:
            self.sendCommand(f"MOVE {move}")
            self.total_distance += float(move)  # Toplam mesafeyi güncelle
            self.positionLabel.setText(f'Absolute Position: {self.total_distance:.2f} mm')

        self.sendCommand("START")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MotorControlApp()
    ex.show()
    sys.exit(app.exec_())
