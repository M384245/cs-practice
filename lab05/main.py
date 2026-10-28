import sys
from logstats import count_levels, top_errors, format_report

def main():
    filename = sys.stdin.readline().strip()
    if not filename:
        return

    with open(filename, encoding="utf-8") as f:
        counts = count_levels(f)
        
    with open(filename, encoding="utf-8") as f:
        errors = top_errors(f, 3)

    total_parsed = sum(v for k, v in counts.items() if k != "BROKEN")
    error_count = counts.get("ERROR", 0)
    broken_count = counts.get("BROKEN", 0)

    print(total_parsed)
    print(error_count)
    print(broken_count)

    report_text = format_report(counts, errors)
    with open("report.txt", "w", encoding="utf-8") as out:
        out.write(report_text)

if __name__ == "__main__":
    main()