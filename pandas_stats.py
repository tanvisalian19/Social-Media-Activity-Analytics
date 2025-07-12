import pandas as pd


def analyze_dataset(file_path, dataset_name):
    print(f"\n\n==================== Analyzing: {dataset_name} ====================\n")

    df = pd.read_csv(file_path)
    print(f" Shape: {df.shape}")
    print(f" Columns: {df.columns.tolist()}")

    # ----------------------------
    # 1. Overall Descriptive Stats
    # ----------------------------
    print("\n--- Overall Descriptive Statistics ---")
    print(df.describe(include='all'))  # Removed datetime_is_numeric parameter

    print("\n--- Unique Values Per Column ---")
    print(df.nunique())

    print("\n--- Most Frequent Values Per Column ---")
    for col in df.columns:
        print(f"\nMost frequent in '{col}':")
        print(df[col].value_counts(dropna=False).head(3))

    # ----------------------------
    # 2. Platform-specific grouping
    # ----------------------------

    # Identify potential ID columns
    id_columns = []
    potential_ids = ['page_id', 'ad_id', 'user_id', 'tweet_id', 'post_id', 'account_id']

    for col in potential_ids:
        if col in df.columns:
            id_columns.append(col)

    print(f"\n--- Available ID columns: {id_columns} ---")

    # Group by the first available ID column
    if id_columns:
        primary_id = id_columns[0]
        print(f"\n--- Grouped by '{primary_id}' (first 3 groups) ---")
        grouped = df.groupby(primary_id)
        group_count = 0
        for group_name, group_df in grouped:
            print(f"\n📌 Group: {group_name}")
            print(f"   Size: {len(group_df)} rows")
            print(f"   Sample columns: {group_df.columns[:5].tolist()}")
            # Show basic stats for numeric columns only to avoid clutter
            numeric_cols = group_df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                print(f"   Numeric summary:")
                print(group_df[numeric_cols].describe())
            group_count += 1
            if group_count >= 3:
                break

        # If we have multiple ID columns, try grouping by the first two
        if len(id_columns) >= 2:
            print(f"\n--- Grouped by ('{id_columns[0]}', '{id_columns[1]}') (first 3 groups) ---")
            grouped_combo = df.groupby([id_columns[0], id_columns[1]])
            combo_count = 0
            for group_name, group_df in grouped_combo:
                print(f"\n📌 Group: {group_name}")
                print(f"   Size: {len(group_df)} rows")
                combo_count += 1
                if combo_count >= 3:
                    break
    else:
        print("\n⚠️ No common ID columns found. Skipping grouped analysis.")

    # ----------------------------
    # 3. Data type analysis
    # ----------------------------
    print("\n--- Data Types Analysis ---")
    print(df.dtypes.value_counts())

    # Check for missing values
    print("\n--- Missing Values ---")
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
    if len(missing_data) > 0:
        print(missing_data)
    else:
        print("No missing values found!")


# ----------------------------
# Analyze All Datasets
# ----------------------------
if __name__ == "__main__":
    datasets = {
        "Facebook Ads": "2024_fb_ads_president_scored_anon.csv",
        "Facebook Posts": "2024_fb_posts_president_scored_anon.csv",
        "Twitter Posts": "2024_tw_posts_president_scored_anon.csv"
    }

    for name, path in datasets.items():
        analyze_dataset(path, name)
