import sys
from stats import read_valid, average_by_city, warmest_city

def main():
    lines = sys.stdin.read().splitlines()
    
    records = read_valid(lines)
    averages = average_by_city(records)
    best_city = warmest_city(records)
    
    empty_lines = sum(1 for line in lines if line.strip() == "")
    skipped = len(lines) - empty_lines - len(records)
    
    print(len(records))
    print(skipped)
    if best_city:
        print(f"{averages[best_city]:.1f}")
    else:
        print("0.0")

if __name__ == "__main__":
    main()