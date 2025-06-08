# Customer Experience Analytics for Fintech Apps – Week 2 Challenge

## Overview
This project analyzes customer satisfaction with mobile banking apps by scraping and processing Google Play Store reviews for three major Ethiopian banks:
- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

The main goal is to identify sentiment, key themes, and improvement opportunities to enhance customer retention and satisfaction.



## Data Collection and Preprocessing

### Data Collection
- Used the [`google-play-scraper`](https://pypi.org/project/google-play-scraper/) Python library to collect reviews.
- Targeted a minimum of **400 reviews per bank** (~1,200 total).
- Scraped data includes:
  - **Review text**
  - **Rating (1–5)**
  - **Date**
  - **Bank name**
  - **Source (Google Play Store)**

### Preprocessing
- Removed duplicate entries.
- Handled missing data (e.g., dropped empty reviews).
- Normalized date format to `YYYY-MM-DD`.
- Saved the cleaned dataset as a CSV file: `cleaned_reviews.csv`.


---

## Next Steps
- Perform sentiment and thematic analysis.
- Store the processed data in an Oracle database.
- Create visualizations and actionable insights for banks.


## Setup
Install the required libraries using:
```bash
pip install -r requirements.txt
