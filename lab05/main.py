import sys
from logstats import count_levels, top_errors, format_report

def main():
    filename = sys.stdin.readline().strip()
    if not filename:
        return

    # 1. Считаем общее количество строк в файле
    with open(filename, encoding="utf-8") as f:
        total_lines = sum(1 for _ in f)

    # 2. Считаем уровни и испорченные строки
    with open(filename, encoding="utf-8") as f:
        counts = count_levels(f)
        
    # 3. Ищем частые ошибки
    with open(filename, encoding="utf-8") as f:
        errors = top_errors(f, 3)

    # 4. Формируем вывод
    broken_count = counts.get("BROKEN", 0)
    error_count = counts.get("ERROR", 0)
    
    # "Разобрано всего" = все строки минус испорченные
    total_parsed = sum(counts.values())

    print(total_parsed)
    print(error_count)
    print(broken_count)

    # 5. Записываем отчет
    report_text = format_report(counts, errors)
    with open("report.txt", "w", encoding="utf-8") as out:
        out.write(report_text)

if __name__ == "__main__":
    main()