import csv
import io
import json

def csv_to_records(text):
    if not text.strip():
        return []
    
    f = io.StringIO(text.strip())
    reader = csv.reader(f)
    
    try:
        # Очищаем заголовки от пробелов по краям
        headers = [h.strip() for h in next(reader)]
    except StopIteration:
        return []
        
    records = []
    for row in reader:
        if not row:
            continue
        # Очищаем значения от пробелов
        row = [r.strip() for r in row]
        # Собираем словарь
        record = {headers[i]: (row[i] if i < len(row) else "") for i in range(len(headers))}
        records.append(record)
    return records

def parse_settings(lines):
    result = {}
    for line in lines:
        # Удаляем всё, что после решетки (комментарии), и пробелы
        line = line.split('#')[0].strip()
        if not line or ':' not in line:
            continue
            
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        
        # Проверяем, может быть, это готовый JSON-список (например, ["город", "цена"])
        if val.startswith('[') and val.endswith(']'):
            try:
                result[key] = json.loads(val)
                continue
            except Exception:
                pass
        
        lower_val = val.lower()
        if lower_val == 'true':
            result[key] = True
        elif lower_val == 'false':
            result[key] = False
        elif lower_val == 'null':
            result[key] = None
        else:
            # Пытаемся распознать числа
            try:
                result[key] = int(val)
            except ValueError:
                try:
                    # Если есть запятая и это число (например, "3,5")
                    if ',' in val and val.replace(',', '').replace('-', '').replace('.', '').isdigit():
                        result[key] = float(val.replace(',', '.'))
                    else:
                        raise ValueError
                except ValueError:
                    # Если не число, но есть запятые, значит это список строк
                    if ',' in val:
                        # Очищаем от возможных кавычек и делаем список
                        items = [item.strip().strip('"\'') for item in val.split(',')]
                        result[key] = items
                    else:
                        # Просто текст, убираем кавычки, если есть
                        result[key] = val.strip('"\'')
    return result

def merge_by_key(left, right, key="id"):
    # Делаем копию левого списка
    result = [dict(rec) for rec in left]
    left_indexes = {rec[key]: i for i, rec in enumerate(result) if key in rec}
    
    # right — это словарь! Перебираем его через items()
    for r_key, r_dict in right.items():
        if r_key in left_indexes:
            # Если ключ есть в левом списке, обновляем словарь
            idx = left_indexes[r_key]
            result[idx].update(r_dict)
        else:
            # Если нет, добавляем как новый элемент, не забыв добавить сам ключ
            new_dict = dict(r_dict)
            new_dict[key] = r_key
            result.append(new_dict)
    return result

def records_to_json(records):
    # ОБЯЗАТЕЛЬНО: indent=2 (отступы) и sort_keys=True (сортировка ключей)
    return json.dumps(records, indent=2, ensure_ascii=False, sort_keys=True)