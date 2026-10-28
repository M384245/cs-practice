def parse_event(line):
    line = line.strip()
    if not line:
        raise ValueError("Empty line")

    parts = line.split(maxsplit=2)
    if len(parts) < 2:
        raise ValueError("Not enough parts")

    time = parts[0]
    level = parts[1]
    message = parts[2] if len(parts) == 3 else ""

    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
    if level not in valid_levels:
        raise ValueError("Invalid level")

    return {"time": time, "level": level, "message": message}


def count_levels(lines):
    counts = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
            lvl = event["level"]
            counts[lvl] = counts.get(lvl, 0) + 1
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
    return counts

def top_errors(lines, n):
    errors = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
            if event["level"] == "ERROR":
                msg = event["message"]
                errors[msg] = errors.get(msg, 0) + 1
        except ValueError:
            pass
    
    sorted_errors = sorted(errors.items(), key=lambda x: (-x[1], x[0]))
    return [[msg, count] for msg, count in sorted_errors[:n]]

def format_report(counts, errors):
    lines = ["Отчёт по журналу", ""]
    for level in sorted(counts.keys()):
        lines.append(f"{level}: {counts[level]}")
    
    lines.append("")
    lines.append("Частые ошибки:")
    for msg, count in errors:
        lines.append(f"- {msg} — {count}")
    
    lines.append("") 
    return "\n".join(lines)