def count_by_extension(paths):
    result = {}
    for p in paths:
        # Отделяем имя файла от пути (на случай, если в папках есть точки)
        filename = p.split('/')[-1]
        parts = filename.split('.')
        # Проверяем, что расширение есть и оно не пустое
        if len(parts) > 1 and parts[-1]:
            ext = parts[-1].lower()
            result[ext] = result.get(ext, 0) + 1
    return result

def deepest_path(paths):
    if not paths:
        return ""
    # Сортируем по алфавиту, чтобы при равенстве глубины сработало правило "первый по алфавиту"
    sorted_paths = sorted(paths)
    max_depth = -1
    best_path = ""
    for p in sorted_paths:
        depth = p.count('/')
        if depth > max_depth:
            max_depth = depth
            best_path = p
    return best_path

def human_size(n_bytes):
    if n_bytes < 1024:
        return f"{n_bytes} B"
    elif n_bytes < 1024**2:
        return f"{n_bytes / 1024:.1f} KB"
    elif n_bytes < 1024**3:
        return f"{n_bytes / (1024**2):.1f} MB"
    else:
        return f"{n_bytes / (1024**3):.1f} GB"