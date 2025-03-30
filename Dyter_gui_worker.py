import sys
import threading

from PyQt5.QtCore import pyqtSignal, QObject

from Dyter import VideoDownloader


# Класс для работы с потоками
class DownloadWorker(QObject):
    update_progress_signal = pyqtSignal(int) # Сигнал для обновления прогресса
    finished_signal = pyqtSignal(list) # Сигнал для завершения загрузки


    def __init__(self, urls, only_audio_flag):
        super().__init__()
        self.urls = urls
        self.only_audio_flag = only_audio_flag


    def run(self):
        tries_count = 5
        video_list = [VideoDownloader(url) for url in self.urls]

        attempt = 0
        while attempt < tries_count and video_list:
            print(f"Попытка {attempt + 1} из {tries_count}")
            remaining_videos = []

            for video in video_list:
                if self.only_audio_flag:
                    flag = video.download_audio()
                else:
                    flag = video.download_video()

                if flag:
                    print(f"Файл {video.title} успешно загружен.")
                    self.update_progress_signal.emit(1)
                else:
                    print(f"Ошибка загрузки файла {video.title}.")
                    remaining_videos.append(video)

            video_list = remaining_videos
            attempt += 1

        rem_urls = []
        if video_list:
            print("Не удалось загрузить следующие файлы после всех попыток:")
            for video in video_list:
                print(video.title)
                rem_urls.append(video.url)
        else:
            print("Все файлы успешно загружены.")

        # Сигнал о завершении загрузки
        self.finished_signal.emit(rem_urls)
