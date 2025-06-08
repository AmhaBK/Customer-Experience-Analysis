from google_play_scraper import reviews, Sort
import pandas as pd

# --- Step 1: Define bank apps and IDs
bank_apps = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp'
}

# --- Step 2: Scrape reviews for each bank
all_reviews = []

for bank_name, app_id in bank_apps.items():
    print(f"Scraping reviews for {bank_name}...")

    result, _ = reviews(
        app_id,
        lang='en',
        country='et',        # Ethiopia country code
        sort=Sort.NEWEST,
        count=400            # Adjust as needed
    )

    # Convert to DataFrame
    df = pd.DataFrame(result)
    
    # Select relevant columns and add metadata
    df_cleaned = df[['content', 'score', 'at']].copy()
    df_cleaned['bank'] = bank_name
    df_cleaned['source'] = 'Google Play'

    # Append to the list
    all_reviews.append(df_cleaned)

print("Scraping complete for all banks.")

# --- Step 3: Combine all DataFrames
combined_df = pd.concat(all_reviews, ignore_index=True)

# --- Step 4: Preprocess - Remove duplicates and handle missing data
combined_df.drop_duplicates(subset=['content'], inplace=True)
combined_df.dropna(subset=['content', 'score', 'at'], inplace=True)

# Normalize date format
combined_df['date'] = pd.to_datetime(combined_df['at']).dt.strftime('%Y-%m-%d')

# Rename columns
combined_df.rename(columns={'content': 'review', 'score': 'rating'}, inplace=True)

# Drop the old 'at' column
combined_df.drop(columns=['at'], inplace=True)

# --- Step 5: Save as CSV
combined_df.to_csv('cleaned_reviews.csv', index=False)

print("Preprocessing complete. Cleaned data saved to 'cleaned_reviews.csv'.")
