from homeharvest import scrape_property
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
ARCHIVE_DIR = DATA_DIR / "archive"

DATA_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(exist_ok=True)

current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
today_date = datetime.now().strftime("%Y-%m-%d")

listings = scrape_property(
    location="Virginia",
    listing_type="for_sale",
    past_days=7
)

listings["scrape_timestamp"] = current_timestamp

# 1. Save timestamped archive copy
archive_file = ARCHIVE_DIR / f"virginia_housing_raw_{today_date}.csv"
listings.to_csv(archive_file, index=False)

# 2. Save latest copy for dashboard
latest_file = DATA_DIR / "virginia_housing_raw.csv"
listings.to_csv(latest_file, index=False)

print(f"Saved latest file: {latest_file}")
print(f"Saved archive file: {archive_file}")
print(f"Rows: {len(listings)}")