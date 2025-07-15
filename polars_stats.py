import polars as pl
import json


def summarize_column(data: pl.DataFrame, column: str) -> dict:
    col_data = data[column].drop_nulls()
    summary = {"count": col_data.len()}

    
    try:
        avg = col_data.mean()
        if avg is not None:
            summary.update({
                "mean": float(avg),
                "stddev": float(col_data.std()),
                "min": float(col_data.min()),
                "max": float(col_data.max())
            })
            return summary
    except Exception:
        pass  

    
    summary["unique"] = col_data.n_unique()
    try:
        freq_df = col_data.value_counts().sort("counts", descending=True)
        summary["most_common"] = str(freq_df[0, column])
        summary["most_common_count"] = int(freq_df[0, "counts"])
    except Exception:
        pass

    return summary


def display_stats(column: str, metrics: dict):
    print(f"\nColumn: {column}")
    for key in [
        "count", "mean", "stddev", "min", "max",
        "unique", "most_common", "most_common_count"
    ]:
        if key in metrics:
            print(f"{key:<24}: {metrics[key]}")
    print("-" * 60)


def inspect_file(file_path: str, dataset_name: str) -> dict:
    print(f"\n=== Inspecting Dataset: {dataset_name} ===")
    df = pl.read_csv(file_path)
    column_stats = {}

    for field in df.columns:
        if df[field].drop_nulls().is_empty():
            continue
        stats = summarize_column(df, field)
        display_stats(field, stats)
        column_stats[field] = stats

    return column_stats


def main():
    summary_results = {}

    summary_results["facebook_ads"] = inspect_file(
        r"C:\Users\Sathvik\Downloads\2024_fb_ads_president_scored_anon.csv",
        "Facebook Ads"
    )

    summary_results["facebook_posts"] = inspect_file(
        r"C:\Users\Sathvik\Downloads\2024_fb_posts_president_scored_anon.csv",
        "Facebook Posts"
    )

    summary_results["twitter_posts"] = inspect_file(
        r"C:\Users\Sathvik\Downloads\2024_tw_posts_president_scored_anon.csv",
        "Twitter Posts"
    )

    with open("polars_stats_output.json", "w", encoding="utf-8") as outfile:
        json.dump(summary_results, outfile, indent=2, default=str)

    print("\n Summary saved to 'polars_stats_output.json'")


if __name__ == "__main__":
    main()
