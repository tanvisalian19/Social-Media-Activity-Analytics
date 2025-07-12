# Social-Media-Activity-Analytics
This research project analyzes the social media activity of candidates during the 2024 US presidential election. It provides descriptive statistics and visualizations of posting frequency, engagement metrics, and sentiment trends across platforms like Fb ads, Fb Posts, and Twitter Posts aiming to uncover patterns in digital campaigning strategies.

# Dataset Access
This project uses a dataset containing Facebook ads, Facebook posts, and Twitter posts related to the 2024 U.S. Presidential Election.

**Dataset Access:**  
[Google Drive Link (provided by course)](https://drive.google.com/file/d/1Jq0fPb-tq76Ee_RtM58fT0_M3o-JDBwe/view?usp=sharing)

**Important:**  
This dataset was provided for academic use only. Please do not upload it to GitHub. The data is excluded from this repository using `.gitignore`.

# Summary of Key Findings per Dataset
1. fb_ads
Columns like ad_id and page_id are often skipped in Polars due to unsupported data types.
Spend, impressions, clicks have high variance – large standard deviation, indicating outliers or diverse ad campaigns.
Most common objective: Often "LINK_CLICKS" or "REACH" depending on subset.
Unique advertisers: Moderate — often under 500 (varies by sample).

2. fb_posts
message field: Very high cardinality (many unique messages), as expected.
Most common page_name: Likely a few recurring political pages.
High engagement skew: A few posts dominate in likes/shares/comments.
Timestamps: Peak posting times may be extracted later.

3. twitter_posts
Tweet text: Nearly all are unique.
Top hashtags: Useful to cluster topics — often reveals focus on specific events (e.g., elections, policy).
Verified accounts: Count is relatively low compared to total.
Language field: English dominates, but multilingual presence may exist.

# Interesting Insights 
High Skew in Metrics → 	Across ads and posts, variables like clicks, impressions, likes, and shares are heavily right-skewed — very few posts/ads drive most of the engagement.
Text Fields → Unique Explosion	Fields like message, tweet_text, and ad_creative_body are mostly unique, making them great candidates for NLP or clustering, but not for simple aggregation.
Campaign Objective Trends	→ The most frequent Facebook Ad objective was consistently "LINK_CLICKS" → signaling a common strategy to drive traffic.
Platform Bias → Twitter had more informational text, while Facebook Posts and Ads leaned more toward calls to action and engagement.
Efficiency → Polars outperforms in speed and memory, while Pandas offers more detailed control and integration with external libraries. Pure Python is educational, but impractical at scale.

# Final Takeaways:
- Use Polars for fast EDA and large datasets.
- Use Pandas when you need easy integrations (visualization, modeling).
- Use Pure Python for building intuition, or small file manipulations.


