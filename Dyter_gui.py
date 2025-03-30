import sys
import threading

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QProgressBar, QCheckBox
from PyQt5.QtWidgets import QSystemTrayIcon

from Dyter import VideoDownloader
from Dyter_gui_worker import DownloadWorker


class DownloadApp(QWidget):
    # Сигнал для обновления прогресса
    update_progress_signal = pyqtSignal(int)
    # Сигнал для завершения загрузки
    finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        # Установка заголовка окна
        self.setWindowTitle('Dyter')

        # Устанавливаем иконку приложения
        self.setWindowIcon(QIcon('resources\img\download_24dp_000000.svg'))

        # Создание элементов GUI
        self._create_ui()
        
        # Чтение CSS-файла
        with open("resources\styles.css", "r") as file:
            stylesheet = file.read()
        
        # Применение стилей ко всему приложению
        self.setStyleSheet(stylesheet)

        # Установка размера окна (ширина, высота)
        self.resize(550, 300)


    def _create_ui(self):
        # Создание многострочного поля ввода текста
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Input YouTube video urls...")

        # Создание чек-бокса "Only audio"
        self.only_audio_checkbox = QCheckBox('Only audio', self)
        self.only_audio_checkbox.stateChanged.connect(self.update_audio_flag)

        # Переменная-флаг для хранения состояния чек-бокса
        self.only_audio_flag = False

        # Создание кнопки "Download"
        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.start_download)

        # Создание индикатора загрузки
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        # Установка вертикального layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.only_audio_checkbox)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)


    def update_audio_flag(self, state):
        # Обновление переменной-флага в зависимости от состояния чек-бокса
        self.only_audio_flag = state == 2  # 2 соответствует состоянию "Checked"


    def start_download(self):
        # Блокировка активных элементов
        self.download_button.setEnabled(False)
        self.text_edit.setEnabled(False)
        self.only_audio_checkbox.setEnabled(False)

        # Получение текста из QTextEdit построчно
        text = self.text_edit.toPlainText()  # Получаем весь текст
        urls = text.splitlines()  # Разделяем текст на строки

        # Инициализация прогресс-бара
        self.progress_bar.setMaximum(len(urls))  # Максимальное значение = количество URL
        self.progress_bar.setValue(0)  # Начинаем с 0

        # Создание и запуск потока
        self.worker = DownloadWorker(urls, self.only_audio_checkbox.isChecked())
        self.worker_thread = threading.Thread(target=self.worker.run)
        self.worker_thread.start()

        # Подключение сигналов
        self.worker.update_progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_finished)


    def update_progress(self, value):
        # Обновление прогресс-бара
        self.progress_bar.setValue(self.progress_bar.value() + value)


    def on_finished(self, result_list):
        # Разблокировка активных элементов после завершения загрузки
        self.download_button.setEnabled(True)
        self.text_edit.setEnabled(True)
        self.only_audio_checkbox.setEnabled(True)

        # Вывод списка строк в QTextEdit
        self.text_edit.clear()
        for line in result_list:
            self.text_edit.append(line)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloadApp()
    ex.show()
    sys.exit(app.exec_())
