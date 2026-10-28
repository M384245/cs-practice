import csv
import io
import json

def csv_to_records(text):
    if not text.strip():
        return []
    
    f = io.StringIO(text.strip())
    reader = csv.reader(f)
    
    try:
        headers = next(reader)
    except StopIteration:
        return []
        
    records = []
    for row in reader:
        if not row:
            continue
        # Если строка короче заголовков, дополняем пустыми строками
        record = {headers[i]: (row[i] if i < len(row) else "") for i in range(len(headers))}
        records.append(record)
    return records

def parse_settings(lines):
    result = {}
    for line in lines:
        line = line.strip()
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith('#'):
            continue
            
        if ':' not in line:
            continue
            
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        
        # Приведение типов
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
                    result[key] = float(val)
                except ValueError:
                    result[key] = val
    return result

def merge_by_key(left, right, key="id"):
    # Делаем копию, чтобы не менять исходный список
    result = [dict(rec) for rec in left] 
    left_indexes = {}
    
    for i, rec in enumerate(result):
        if key in rec:
            left_indexes[rec[key]] = i
            
    for r_rec in right:
        if key not in r_rec:
            continue
        r_val = r_rec[key]
        
        if r_val in left_indexes:
            idx = left_indexes[r_val]
            result[idx].update(r_rec)
        else:
            result.append(dict(r_rec))
            
    return result

def records_to_json(records):
    # ensure_ascii=False критически важен для сохранения русских букв
    return json.dumps(records, ensure_ascii=False)