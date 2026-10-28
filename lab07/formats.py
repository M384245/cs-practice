import csv
import io
import json
import copy

def csv_to_records(text):
    if not text.strip():
        return []
    
    f = io.StringIO(text.strip())
    reader = csv.reader(f)
    
    try:
        headers = [h.strip() for h in next(reader)]
    except StopIteration:
        return []
        
    records = []
    for row in reader:
        if not row:
            continue
        row = [r.strip() for r in row]
        record = {headers[i]: (row[i] if i < len(row) else "") for i in range(len(headers))}
        records.append(record)
    return records

def parse_settings(lines):
    result = {}
    for line in lines:
        # Отрезаем комментарии и пробелы
        line = line.split('#')[0].strip()
        if not line or ':' not in line:
            continue
            
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        
        # 1. Списки в квадратных скобках
        if val.startswith('[') and val.endswith(']'):
            inner = val[1:-1].strip()
            if not inner:
                result[key] = []
            else:
                result[key] = [item.strip().strip('"\'') for item in inner.split(',')]
            continue
            
        lower_val = val.lower()
        if lower_val == 'true':
            result[key] = True
        elif lower_val == 'false':
            result[key] = False
        elif lower_val == 'null':
            result[key] = None
        else:
            # 2. Пробуем int
            try:
                result[key] = int(val)
                continue
            except ValueError:
                pass
                
            # 3. Пробуем float (с точкой или запятой)
            try:
                clean_val = val.replace(',', '.').replace(' ', '')
                result[key] = float(clean_val)
                continue
            except ValueError:
                pass
                
            # 4. Если не число, но есть запятая (без скобок) — делаем список
            if ',' in val:
                result[key] = [item.strip().strip('"\'') for item in val.split(',')]
            else:
                result[key] = val.strip('"\'')
    return result

def merge_by_key(left, right, key="id"):
    # Делаем глубокую копию, чтобы не менять исходный список
    result = copy.deepcopy(left)
    
    # Собираем ключи, которые уже есть в левом списке
    left_keys = {str(rec[key]) for rec in result if key in rec}
    
    # 1. Обновляем существующие элементы
    for rec in result:
        if key in rec:
            r_key = str(rec[key])
            if r_key in right:
                rec.update(right[r_key])
            elif rec[key] in right:
                rec.update(right[rec[key]])
                
    # 2. Добавляем новые элементы из right, которых не было в left
    for r_key, r_dict in right.items():
        if str(r_key) not in left_keys:
            new_dict = {key: r_key}
            new_dict.update(r_dict)
            result.append(new_dict)
            
    return result

def records_to_json(records):
    return json.dumps(records, indent=2, ensure_ascii=False, sort_keys=True)