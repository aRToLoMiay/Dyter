import os
import re


def clean_filename(filename):
    """
    Очищает имя файла от недопустимых символов и лишних пробелов.

    Параметры:
    ----------
    filename : str
        Исходное имя файла, которое может содержать недопустимые символы.

    Возвращает:
    -----------
    str
        Очищенное имя файла. Если после очистки имя файла становится пустым,
        возвращается значение по умолчанию "default_filename.txt".

    Пример:
    -------
    >>> clean_filename('my/file:name?.txt')
    'myfilename.txt'
    """
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    cleaned_filename = re.sub(invalid_chars, '', filename)
    cleaned_filename = cleaned_filename.strip()
    return cleaned_filename if cleaned_filename else "default_filename"


def delete_file(file_name):
    """
    Удаляет указанный файл, если он существует. В случае ошибки выводит сообщение.

    Параметры:
    ----------
    file_name : str
        Имя файла, который необходимо удалить.

    Возвращает:
    -----------
    None
        Функция не возвращает значений, но выводит сообщения о результате операции.

    Пример:
    -------
    >>> delete_file("example.txt")
    Файл 'example.txt' был успешно удалён.
    """
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Файл '{file_name}' был успешно удалён.")
        else:
            print(f"Файл '{file_name}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при попытке удалить файл: {e}")

        
def read_file_lines(file_name):
    """
    Читает все строки из указанного файла и возвращает их в виде списка.

    Параметры:
    ----------
    file_name : str
        Имя файла, который необходимо прочитать.

    Возвращает:
    -----------
    list
        Список строк, прочитанных из файла. Каждая строка очищена от лишних пробелов
        и символов перевода строки. Если файл не найден или произошла ошибка,
        возвращается пустой список.

    Пример:
    -------
    >>> lines = read_file_lines("example.txt")
    >>> print(lines)
    ['Первая строка', 'Вторая строка', 'Третья строка']
    """
    lines = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append(line.strip())
    except FileNotFoundError:
        print(f"Файл '{file_name}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return lines
