import os

def count_by_extension(paths):
    result = {}
    for p in paths:
        # Отделяем имя файла от пути
        filename = os.path.basename(p)
        # Стандартный метод отделения расширения. 
        # Для ".gitignore" вернет ('', '.gitignore'), но так как мы убираем точку, получится "".
        _, ext = os.path.splitext(filename)
        ext = ext.lstrip('.').lower()
        result[ext] = result.get(ext, 0) + 1
    return result

def deepest_path(paths):
    if not paths:
        return ""
    # Сортируем пути по алфавиту
    sorted_paths = sorted(paths)
    # Ищем максимальную глубину
    max_depth = max((p.count('/') for p in sorted_paths), default=0)
    # Возвращаем первый путь, который достиг этой глубины (он будет первым по алфавиту)
    for p in sorted_paths:
        if p.count('/') == max_depth:
            return p
    return ""

def human_size(n_bytes):
    if n_bytes < 1024:
        return f"{n_bytes} Б"
    elif n_bytes < 1024**2:
        return f"{n_bytes / 1024:.1f} КБ"
    elif n_bytes < 1024**3:
        return f"{n_bytes / (1024**2):.1f} МБ"
    else:
        return f"{n_bytes / (1024**3):.1f} ГБ"