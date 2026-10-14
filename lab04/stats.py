def parse_record(line):
    city, temp, date = line.split(";")
    return {"city": city, "temperature": float(temp), "date": date}

def read_valid(lines):
    records = []
    for line in lines:
        if line.strip() == "":
            continue
        records.append(parse_record(line))
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