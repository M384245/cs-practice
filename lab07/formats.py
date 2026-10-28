# Lab 07 Final Working Version
import csv
import io
import json

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
        line = line.split('#')[0].strip()
        if not line or ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()

        if not val:
            result[key] = None
            continue

        if val.lower() == 'true':
            result[key] = True
        elif val.lower() == 'false':
            result[key] = False
        elif val.lower() == 'null':
            result[key] = None
        elif val.startswith('[') and val.endswith(']'):
            try:
                result[key] = json.loads(val)
            except:
                result[key] = [x.strip().strip('"\'') for x in val[1:-1].split(',') if x.strip()]
        elif ',' in val:
            try:
                result[key] = float(val.replace(',', '.'))
            except ValueError:
                result[key] = [x.strip().strip('"\'') for x in val.split(',')]
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
    import copy
    result = copy.deepcopy(left) # Глубокая копия для безопасности
    
    if isinstance(right, dict):
        items = right.items()
    elif isinstance(right, list):
        items = [(r.get(key), r) for r in right if key in r]
    else:
        return result

    for r_key, r_val in items:
        found = False
        for item in result:
            if str(item.get(key)) == str(r_key):
                item.update(r_val)
                found = True
                break
        if not found:
            new_item = {key: r_key}
            new_item.update(r_val)
            result.append(new_item)
    return result

def records_to_json(records):
    return json.dumps(records, indent=2, ensure_ascii=False, sort_keys=True)
