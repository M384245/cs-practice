def parse_record(line):
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError("Неверное количество полей")
    
    city, temp_str, date = parts
    if not city.strip() or not date.strip():
        raise ValueError("Пустой город или дата")
    
    try:
        temp = float(temp_str.strip().replace(",", "."))
    except ValueError:
        raise ValueError("Температура не является числом")
    
    return {"city": city.strip(), "temperature": temp, "date": date.strip()}

def read_valid(lines):
    records = []
    for line in lines:
        if line.strip() == "":
            continue
        
        try:
            records.append(parse_record(line))
        except ValueError:
            continue
            
    return records

def average_by_city(records):
    city_temps = {}
    for rec in records:
        city = rec["city"]
        if city not in city_temps:
            city_temps[city] = []
        city_temps[city].append(rec["temperature"])
    
    result = {}
    for city, temps in city_temps.items():
        result[city] = round(sum(temps) / len(temps), 1)
    return result

def warmest_city(records):
    averages = average_by_city(records)
    if not averages:
        return ""
    best = sorted(averages.items(), key=lambda item: (-item[1], item[0]))
    return best[0][0]