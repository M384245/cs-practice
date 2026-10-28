import csv
import io
import json

def csv_to_records(text):
    if not text.strip():
        return []
    
    f = io.StringIO(text.strip())
    reader = csv.reader(f)
    
    try:
        # Очищаем заголовки от пробелов
        headers = [h.strip() for h in next(reader)]
    except StopIteration:
        return []
        
    records = []
    for row in reader:
        if not row:
            continue
        # Очищаем значения от пробелов
        row = [r.strip() for r in row]
        record = {headers[i]: (row[i] if i < len(row) else "") for i in range(len(headers))}
        records.append(record)
    return records

def parse_settings(lines):
    result = {}
    for line in lines:
        # Удаляем комментарии (все, что после #)
        line = line.split('#')[0].strip()
        if not line or ':' not in line:
            continue
            
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        
        lower_val = val.lower()
        if lower_val == 'true':
            result[key] = True
        elif lower_val == 'false':
            result[key] = False
        elif lower_val == 'null':
            result[key] = None
        else:
            try:
                result[key] = int(val)
            except ValueError:
                try:
                    # Проверяем на float с запятой (например, 3,5)
                    if ',' in val and val.replace(',', '').replace('-', '').replace('.', '').isdigit():
                        result[key] = float(val.replace(',', '.'))
                    else:
                        raise ValueError
                except ValueError:
                    # Если есть запятые (город, цена), делаем список
                    if ',' in val:
                        result[key] = [item.strip() for item in val.split(',')]
                    else:
                        result[key] = val
    return result

def merge_by_key(left, right, key="id"):
    # Делаем копию левого списка
    result = [dict(rec) for rec in left]
    # Запоминаем, под каким индексом лежит каждый id
    left_indexes = {rec[key]: i for i, rec in enumerate(result) if key in rec}
    
    # right — это СЛОВАРЬ! Перебираем его items()
    for r_key, r_dict in right.items():
        if r_key in left_indexes:
            idx = left_indexes[r_key]
            result[idx].update(r_dict)
        else:
            # Если нет в левом, добавляем как новый (не забываем добавить id)
            new_dict = dict(r_dict)
            new_dict[key] = r_key
            result.append(new_dict)
    return result

def records_to_json(records):
    # indent=2 для красивых отступов, sort_keys=True для сортировки букв
    return json.dumps(records, indent=2, ensure_ascii=False, sort_keys=True)