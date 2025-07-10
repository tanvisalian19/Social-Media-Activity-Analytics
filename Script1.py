import csv
import math
from collections import defaultdict, Counter

def load_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

def is_number(value):
    """ Checking if a string can be converted to a float."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def compute_stats(data):
    """Computing descriptive statistics for each column in the dataset."""
    if not data:
        return {}

    stats = {}
    columns = data[0].keys()

    for col in columns:
        raw_values = [row[col] for row in data if row[col] != '']
        numeric_values = [float(v) for v in raw_values if is_number(v)]

        if numeric_values:
            count = len(numeric_values)
            mean = sum(numeric_values) / count
            min_val = min(numeric_values)
            max_val = max(numeric_values)
            std_dev = math.sqrt(sum((x - mean) ** 2 for x in numeric_values) / count)

            stats[col] = {
                'type': 'numeric',
                'count': count,
                'mean': mean,
                'min': min_val,
                'max': max_val,
                'std_dev': std_dev
            }
        else:
            count = len(raw_values)
            value_counts = Counter(raw_values)
            most_common = value_counts.most_common(1)[0] if value_counts else ("N/A", 0)

            stats[col] = {
                'type': 'non-numeric',
                'count': count,
                'unique_values': len(value_counts),
                'most_frequent': most_common
            }

    return stats

def group_by(data, *group_cols):
    """Grouping the data by one or more specified columns."""
    grouped = defaultdict(list)
    for row in data:
        key = tuple(row[col] for col in group_cols)
        grouped[key].append(row)
    return grouped

def print_stats(label, stats):
    """Printing computed statistics for a dataset or group."""
    print(f"\n--- {label} ---")
    for col, stat in stats.items():
        print(f"\nColumn: {col}")
        for k, v in stat.items():
            print(f"  {k}: {v}")

def run_analysis(file_path):
    data = load_csv(file_path)

    # Overall dataset stats
    overall_stats = compute_stats(data)
    print_stats("Overall Dataset", overall_stats)

    # Grouped by page_id
    grouped_page = group_by(data, 'page_id')
    for group, records in list(grouped_page.items())[:3]:  # print first 3 groups
        group_stats = compute_stats(records)
        print_stats(f"Group by page_id: {group}", group_stats)

    # Grouped by (page_id, ad_id)
    ad_id_exists = 'ad_id' in data[0]
    if ad_id_exists:
        grouped_combined = group_by(data, 'page_id', 'ad_id')
        for group, records in list(grouped_combined.items())[:3]:  # print first 3 groups
            group_stats = compute_stats(records)
            print_stats(f"Group by (page_id, ad_id): {group}", group_stats)
    else:
        print("\n'ad_id' column not found, skipping (page_id, ad_id) grouping.")

if __name__ == "__main__":
    filepath = "2024_fb_posts_president_scored_anon.csv"
    run_analysis(filepath)
