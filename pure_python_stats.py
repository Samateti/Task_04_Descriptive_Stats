import csv
import json
import math
from collections import defaultdict, Counter
from typing import Any, Dict, List, Tuple

ADS_FILE = r"C:\Users\Sathvik\Downloads\2024_fb_ads_president_scored_anon.csv"
FB_POSTS_FILE = r"C:\Users\Sathvik\Downloads\2024_fb_posts_president_scored_anon.csv"
TWITTER_FILE = r"C:\Users\Sathvik\Downloads\2024_tw_posts_president_scored_anon.csv"


def read_csv(filepath: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = [col.strip().lower() for col in reader.fieldnames]
        data = []
        for row in reader:
            clean_row = {col.strip().lower(): convert_type(val) for col, val in row.items()}
            data.append(clean_row)
        return headers, data


def convert_type(value: str) -> Any:
    value = value.strip()
    try:
        return float(value)
    except ValueError:
        return value.lower() if isinstance(value, str) else value


def compute_stats(values: List[Any]) -> Dict[str, Any]:
    numerics = [v for v in values if isinstance(v, float)]
    categoricals = [v for v in values if not isinstance(v, float)]
    summary = {'count': len(values)}

    if numerics:
        mean_val = sum(numerics) / len(numerics)
        stddev = math.sqrt(sum((x - mean_val) ** 2 for x in numerics) / (len(numerics) - 1)) if len(numerics) > 1 else 0.0
        summary.update(mean=mean_val, min=min(numerics), max=max(numerics), stddev=stddev)

    if categoricals:
        freq_counter = Counter(categoricals)
        top_cat, top_count = freq_counter.most_common(1)[0]
        summary.update(unique=len(freq_counter), most_common=top_cat, most_common_count=top_count)

    return summary


def analyze_columns(headers: List[str], data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    col_values = defaultdict(list)
    for record in data:
        for key in headers:
            col_values[key].append(record.get(key, None))
    return {col: compute_stats(vals) for col, vals in col_values.items()}


def group_data(records: List[Dict[str, Any]], fields: List[str]) -> Dict[Tuple, List[Dict[str, Any]]]:
    grouped = defaultdict(list)
    for entry in records:
        try:
            group_key = tuple(entry.get(field, "N/A") for field in fields)
            grouped[group_key].append(entry)
        except Exception as e:
            print(f"Grouping error: {e}")
            continue
    return grouped


def analyze_groupings(headers: List[str], records: List[Dict[str, Any]], keys: List[str]) -> Dict:
    grouped_records = group_data(records, keys)
    return {group: analyze_columns(headers, rows) for group, rows in grouped_records.items()}


def summarize_groups(title: str, analysis: Dict, max_groups: int = 3) -> Dict[str, Any]:
    print(f"\n--- {title} ---")
    preview = {}
    for idx, (grp, stats) in enumerate(analysis.items()):
        if idx >= max_groups:
            break
        print(f"\nGroup: {grp}")
        for col, metrics in stats.items():
            print(f"  {col}")
            for k, v in metrics.items():
                print(f"    {k:<18}: {v}")
        print("-" * 60)
        preview[str(grp)] = stats
    return preview


def handle_file(filepath: str, key1: List[str], key2: List[str], label: str) -> Dict[str, Any]:
    headers, records = read_csv(filepath)

    overall_summary = analyze_columns(headers, records)
    group_summary_1 = analyze_groupings(headers, records, key1)
    group_summary_2 = analyze_groupings(headers, records, key2)

    group_sample_1 = summarize_groups(f"{label} – Grouped by {key1}", group_summary_1)
    group_sample_2 = summarize_groups(f"{label} – Grouped by {key2}", group_summary_2)

    return {
        "overall": overall_summary,
        f"grouped_by_{'_'.join(key1)}": group_sample_1,
        f"grouped_by_{'_'.join(key2)}": group_sample_2,
    }


if __name__ == "__main__":
    results = {}

    results["facebook_ads"] = handle_file(
        ADS_FILE, ["page_id"], ["page_id", "ad_id"], "Facebook Ads"
    )

    results["facebook_posts"] = handle_file(
        FB_POSTS_FILE, ["facebook_id"], ["facebook_id", "post_id"], "Facebook Posts"
    )

    results["twitter_posts"] = handle_file(
        TWITTER_FILE, ["twitter_handle"], ["twitter_handle", "post_id"], "Twitter Posts"
    )

    with open("python_stats_output.json", "w", encoding="utf-8") as out_file:
        json.dump(results, out_file, indent=2)

    print("\n Statistics saved to 'python_stats_output.json'")
