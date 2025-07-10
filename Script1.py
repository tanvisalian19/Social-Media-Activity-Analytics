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

def run_analysis(file_path, dataset_name):
    """Run full analysis for a given dataset file and label."""
    print(f"\n\n==================== Analyzing: {dataset_name} ====================")
    data = load_csv(file_path)

    # Overall dataset stats
    overall_stats = compute_stats(data)
    print_stats("Overall Dataset", overall_stats)

    # Check if 'page_id' exists before grouping
    if 'page_id' in data[0]:
        grouped_page = group_by(data, 'page_id')
        for group, records in list(grouped_page.items())[:3]:  # limit to 3 groups
            group_stats = compute_stats(records)
            print_stats(f"Group by page_id: {group}", group_stats)
    else:
        print("\n'page_id' column not found, skipping grouping by page_id.")

    # Check if 'ad_id' exists before grouping
    if 'page_id' in data[0] and 'ad_id' in data[0]:
        grouped_combo = group_by(data, 'page_id', 'ad_id')
        for group, records in list(grouped_combo.items())[:3]:  # limit to 3 groups
            group_stats = compute_stats(records)
            print_stats(f"Group by (page_id, ad_id): {group}", group_stats)
    else:
        print("\nEither 'page_id' or 'ad_id' not found, skipping (page_id, ad_id) grouping.")

if __name__ == "__main__":
    datasets = {
        "Facebook Ads": "2024_fb_ads_president_scored_anon.csv",
        "Facebook Posts": "2024_fb_posts_president_scored_anon.csv",
        "Twitter Posts": "2024_tw_posts_president_scored_anon.csv"
    }

    for name, path in datasets.items():
        run_analysis(path, name)
