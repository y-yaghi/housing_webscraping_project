from homeharvest import scrape_property
from datetime import datetime
from pathlib import Path
import pandas as pd

# ---------------- PATHS ----------------

DATA_DIR = Path("data")
ARCHIVE_DIR = DATA_DIR / "archive"

LATEST_FILE = DATA_DIR / "virginia_housing_raw.csv"

DATA_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------- SCRAPE ----------------

run_time = datetime.now()
today = run_time.strftime("%Y-%m-%d")
timestamp = run_time.strftime("%Y-%m-%d_%H-%M-%S")

print("Starting Realtor scrape...")
print(f"Run time: {timestamp}")

listings = scrape_property(
    location="Virginia",
    listing_type="for_sale",
    past_days=7
)

print(f"Scrape finished. Rows collected: {len(listings):,}")

# ---------------- VALIDATION ----------------

if listings is None or listings.empty:
    raise ValueError("Scrape returned no listings. Keeping existing files unchanged.")

listings["scrape_date"] = today
listings["scrape_timestamp"] = timestamp

# ---------------- SAVE LATEST FILE ----------------

listings.to_csv(LATEST_FILE, index=False)
print(f"Updated latest dashboard file: {LATEST_FILE}")

# ---------------- SAVE ARCHIVE FILE ----------------

archive_file = ARCHIVE_DIR / f"virginia_housing_raw_{today}.csv"

if archive_file.exists():
    archive_file = ARCHIVE_DIR / f"virginia_housing_raw_{timestamp}.csv"

listings.to_csv(archive_file, index=False)
print(f"Saved archive file: {archive_file}")

print("Scraper completed successfully.")