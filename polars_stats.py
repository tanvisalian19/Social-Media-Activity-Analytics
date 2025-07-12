import polars as pl


def analyze_dataset_polars(file_path, dataset_name):
    print(f"\n\n==================== Analyzing: {dataset_name} ====================")

    # Load the dataset
    df = pl.read_csv(file_path)

    # Basic info
    print(f"📌 Shape: {df.shape}")
    print(f"📌 Columns: {df.columns}")

    # Descriptive statistics (numeric columns)
    print("\n--- Descriptive Statistics ---")
    print(df.describe())

    # Unique value counts per column
    print("\n--- Unique Value Counts ---")
    for col in df.columns:
        unique_count = df.select(pl.col(col).n_unique()).item()
        print(f"{col}: {unique_count} unique values")

    # Most frequent values per column (safe for unsupported types)
    print("\n--- Most Frequent Values (Top 3) ---")
    for col in df.columns:
        dtype = df.schema[col]

        # Skip complex data types that can't be easily grouped
        if dtype in [pl.List, pl.Struct, pl.Array]:
            print(f"⚠️ Skipping column '{col}' due to complex data type ({dtype}).")
            continue

        try:
            value_counts = (
                df.group_by(col)
                .agg(pl.len().alias("count"))
                .sort("count", descending=True)  # Changed from reverse=True to descending=True
            )
            print(f"\nTop values for '{col}':")
            print(value_counts.head(3))
        except Exception as e:
            print(f"⚠️ Skipping column '{col}' due to error: {e}")


if __name__ == "__main__":
    datasets = {
        "Facebook Ads": "2024_fb_ads_president_scored_anon.csv",
        "Facebook Posts": "2024_fb_posts_president_scored_anon.csv",
        "Twitter Posts": "2024_tw_posts_president_scored_anon.csv"
    }

    for name, path in datasets.items():
        analyze_dataset_polars(path, name)
