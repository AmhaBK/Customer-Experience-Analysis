from google_play_scraper import reviews, Sort
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Define bank apps and IDs
bank_apps = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp'
}

# Scrape reviews for each bank
all_reviews = []

for bank_name, app_id in bank_apps.items():
    print(f"Scraping reviews for {bank_name}...")

    result, _ = reviews(
        app_id,
        lang='en',
        country='et',        # Ethiopia country code
        sort=Sort.NEWEST,
        count=500            # Adjust as needed
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

# Combine all DataFrames
combined_df = pd.concat(all_reviews, ignore_index=True)

# Preprocess - Remove duplicates and handle missing data
combined_df.drop_duplicates(subset=['content'], inplace=True)
combined_df.dropna(subset=['content', 'score', 'at'], inplace=True)

# Normalize date format
combined_df['date'] = pd.to_datetime(combined_df['at']).dt.strftime('%Y-%m-%d')

# Rename columns
combined_df.rename(columns={'content': 'review', 'score': 'rating'}, inplace=True)

# Drop the old 'at' column
combined_df.drop(columns=['at'], inplace=True)

# Preprocessing function
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)

# Apply preprocessing
combined_df['processed_review'] = combined_df['review'].apply(preprocess_text)

# Correcting spelling mistakes

from spellchecker import SpellChecker

# Initialize the spell checker
spell = SpellChecker()

# Define a list of known words to add
known_words= ['cbe', 'boa', 'abyssinia', 'dashen', 'cbebirr', 'amole', 'fintech', 'mobilebanking', 'otp', 'ui', 'ux', 'superapp', 'app', 'etb', 'birr']
spell.word_frequency.load_words(known_words)
print(f"Added {len(known_words)} known words to the spell checker.")

# Function to correct spelling mistakes
def correct_spelling(text):
    if pd.isna(text) or text.strip() == "":
        return text

    # Convert text to lowercase first for consistent correction
    text_lower = text.lower()
    words = text_lower.split() # Split text into words

    corrected_words = []
    for word in words:
        # Get the corrected word. `correction()` returns the most probable correct spelling.
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word if corrected_word is not None else word) # Use original if no correction found

    return " ".join(corrected_words)

print("\nApplying spell correction to reviews. This might take some time...")

# Apply the spell correction function to the 'processed_review' column

combined_df['corrected_review'] = combined_df['processed_review'].apply(correct_spelling)

print("Spelling correction complete.")

# Drop unecessary columns and minor renaming
combined_df.drop('processed_review', axis=1, inplace=True)

combined_df.rename(columns={'corrected_review': 'processed_review'}, inplace=True)

# Drop rows with missing values
combined_df.dropna(inplace=True)

# Save as CSV
combined_df.to_csv('cleaned_reviews.csv', index=False)

print("Preprocessing complete. Cleaned data saved to 'cleaned_reviews.csv'.")
