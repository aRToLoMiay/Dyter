import os
import sys
import yt_dlp

from file_processor import clean_filename


class VideoDownloader:
    def __init__(self, url=None):
        """
        Конструктор класса. Инициализирует поля класса.
        :param url: URL видео или аудио для загрузки.
        """
        self.set_url(url)


    def set_url(self, url):
        """
        Устанавливает URL для загрузки.
        :param url: URL видео или аудио.
        """
        self.url = url
        self._get_title()


    def download_video(self):
        """
        Загружает видео.
        """
        print(self._get_ffmpeg_path())
        options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',  # Лучшее видео + аудио
            'merge_output_format': 'mp4',  # Объединить в MP4 (требует FFmpeg)
            'outtmpl': '%(title)s.%(ext)s',  # Шаблон имени файла
            'ffmpeg_location': self._get_ffmpeg_path(), # Указываем путь к ffmpeg
            'quiet': True,  # Отключаем вывод лишней информации
        }
        return self._download(options)


    def download_audio(self):
        """
        Загружает аудио.
        """
        options = {
            # Основные параметры
            'format': 'bestaudio/best',  # Выбираем лучшее аудио (любого формата)
            'outtmpl': '%(title)s.%(ext)s',  # Шаблон имени файла
            'ffmpeg_location': self._get_ffmpeg_path(), # Указываем путь к ffmpeg
            'quiet': True,  # Отключаем вывод лишней информации
            # Параметры для MP3
            'postprocessors': [
                # Конвертация в MP3
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',  # Качество (192, 256, 320 кбит/с)
                },
                # Добавление обложки
                {
                    'key': 'EmbedThumbnail',  # Встроить обложку
                    'already_have_thumbnail': False,  # Скачать новую
                },
                # Добавление метаданных
                {
                    'key': 'FFmpegMetadata',  # Добавить теги (название, исполнитель)
                }
            ],
            # Параметры обложки
            'writethumbnail': True,  # Скачать обложку
            'convertthumbnails': 'jpg',  # Конвертировать в JPG (или 'png')
        }
        return self._download(options)


    def _download(self, options):
        """
        Внутренний метод для загрузки файла по URL.
        :param options: YDL-настройки для загрузки.
        """
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([self.url])
            return True
        except Exception as e:
            print(f'Произошла ошибка при загрузке: {e}')
            return False


    def _get_title(self):
        """
        Внутренний метод для получения заголовка видео или аудио.
        """
        ydl_opts = {
            'quiet': True,  # Отключаем вывод лишней информации
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Извлекаем информацию о видео
                info_dict = ydl.extract_info(self.url, download=False)
                # Получаем название видео
                self.title = clean_filename(info_dict.get('title', ''))
        except Exception as e:
            print(f'Произошла ошибка при определении названия: {e}')
            self.title = ''

    
    def _get_ffmpeg_path(self):
        if getattr(sys, 'frozen', False):  # Если в EXE
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        # Формируем путь к ffmpeg (в подпапке bin)
        ffmpeg_path = os.path.join(base_dir, "bin", "ffmpeg")
        # Для Windows добавляем .exe, если его нет в пути
        if sys.platform == "win32" and not ffmpeg_path.endswith(".exe"):
            ffmpeg_path += ".exe"
        return ffmpeg_path
