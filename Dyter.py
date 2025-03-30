from file_processor import clean_filename, delete_file, read_file_lines
from video_downloader import VideoDownloader

def download_to_files(urls, only_audio):
    tries_count = 5

    video_list = []
    for url in urls:
        video = VideoDownloader(url)
        video_list.append(video)

    attempt = 0
    while attempt < tries_count and video_list:
        print(f"Попытка {attempt + 1} из {tries_count}")
        remaining_videos = []
        
        for video in video_list:
            if only_audio:
                flag = video.download_audio()
            else:
                flag = video.download_video()

            if flag:
                print(f"Файл {video.title} успешно загружен.")
            else:
                print(f"Ошибка загрузки файла {video.title}.")
                remaining_videos.append(video)
        
        video_list = remaining_videos
        attempt += 1
    
    if video_list:
        print("Не удалось загрузить следующие файлы после всех попыток:")
        for video in video_list:
            print(video.title)
    else:
        print("Все файлы успешно загружены.")    


if __name__ == '__main__':
    file = "urls.txt"
    urls = read_file_lines(file)
    download_to_files(urls = urls, only_audio=False)
