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
        # Отрезаем комментарии
        line = line.split('#')[0].strip()
        if not line or ':' not in line:
            continue
            
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        
        if val.lower() == 'true':
            result[key] = True
        elif val.lower() == 'false':
            result[key] = False
        elif val.lower() == 'null' or not val:
            result[key] = None
        elif val.startswith('[') and val.endswith(']'):
            try:
                result[key] = json.loads(val)
            except:
                result[key] = val
        elif ',' in val:
            # Проверяем, является ли это числом с запятой (например, 3,5)
            parts = [p.strip() for p in val.split(',')]
            is_float = True
            for p in parts:
                if not p.replace('.', '', 1).replace('-', '', 1).isdigit():
                    is_float = False
                    break
            if is_float:
                result[key] = float(val.replace(',', '.'))
            else:
                # Если не число, значит это список строк
                result[key] = [p.strip('"\'') for p in parts]
        else:
            try:
                result[key] = int(val)
            except ValueError:
                try:
                    result[key] = float(val)
                except ValueError:
                    result[key] = val.strip('"\'')
    return result

def merge_by_key(left, right, key="id"):
    result = copy.deepcopy(left)
    # Словарь для быстрого поиска существующих элементов
    left_dict = {str(rec[key]): rec for rec in result if key in rec}
    
    for r_key, r_dict in right.items():
        r_key_str = str(r_key)
        if r_key_str in left_dict:
            # Если есть, обновляем
            left_dict[r_key_str].update(r_dict)
        else:
            # Если нет, создаем новый и добавляем
            new_rec = {key: r_key}
            new_rec.update(r_dict)
            result.append(new_rec)
    return result

def records_to_json(records):
    return json.dumps(records, indent=2, ensure_ascii=False, sort_keys=True)