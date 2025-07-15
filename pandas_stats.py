import pandas as pd
import json


def summarize_dataframe(df: pd.DataFrame) -> dict:
    summary = {}
    description = df.describe(include='all').T

    for column in df.columns:
        col_summary = {}

        
        if column in description.index:
            stats = description.loc[column]
            col_summary["count"] = int(stats.get("count", 0))

            if "mean" in stats:
                col_summary["mean"] = stats["mean"]
            if "std" in stats:
                col_summary["stddev"] = stats["std"]
            if "min" in stats:
                col_summary["min"] = stats["min"]
            if "max" in stats:
                col_summary["max"] = stats["max"]

        
        if df[column].dtype == object or df[column].dtype.name == "category":
            value_counts = df[column].value_counts(dropna=True)
            if not value_counts.empty:
                col_summary["unique"] = int(df[column].nunique(dropna=True))
                col_summary["most_common"] = value_counts.idxmax()
                col_summary["most_common_count"] = int(value_counts.max())

        summary[column] = col_summary

    return summary


def evaluate_file(file_path: str, dataset_name: str) -> dict:
    print(f"\n=== Processing Dataset: {dataset_name} ===")
    df = pd.read_csv(file_path, encoding="utf-8")
    stats = summarize_dataframe(df)

    for col, metrics in stats.items():
        print(f"\nColumn: {col}")
        for k, v in metrics.items():
            print(f"  {k:<20}: {v}")
        print("-" * 50)

    return stats


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="records")
    elif isinstance(obj, pd.Timestamp):
        return str(obj)
    else:
        return obj


def main():
    summaries = {}

    summaries["facebook_ads"] = evaluate_file(
        r"C:\Users\Sathvik\Downloads\2024_fb_ads_president_scored_anon.csv",
        "Facebook Ads"
    )

    summaries["facebook_posts"] = evaluate_file(
        r"C:\Users\Sathvik\Downloads\2024_fb_posts_president_scored_anon.csv",
        "Facebook Posts"
    )

    summaries["twitter_posts"] = evaluate_file(
        r"C:\Users\Sathvik\Downloads\2024_tw_posts_president_scored_anon.csv",
        "Twitter Posts"
    )

    with open("pandas_stats_output.json", "w", encoding="utf-8") as f:
        json.dump(make_json_safe(summaries), f, indent=2)

    print("\n Summary statistics saved to 'pandas_stats_output.json'")


if __name__ == "__main__":
    main()
