from pymongo import MongoClient
import pandas as pd

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["fastf1"]
laps_collection = db["laps"]

def save_laps_to_mongo(driver_code: str, laps_df: pd.DataFrame):
    """
    Save laps from a DataFrame into MongoDB.
    Each lap is saved as a document with a driver_code field.
    """
    laps = laps_df.to_dict(orient='records')
    for lap in laps:
        lap['driver'] = driver_code
    laps_collection.insert_many(laps)
    print(f"Saved {len(laps)} laps for {driver_code}.")

def load_laps_from_mongo(driver_code: str) -> pd.DataFrame:
    """
    Load laps from MongoDB for a given driver_code.
    Returns a pandas DataFrame.
    """
    cursor = laps_collection.find({"driver": driver_code})
    data = list(cursor)
    if not data:
        print("No data found.")
        return pd.DataFrame()
    for doc in data:
        doc.pop('_id', None)  # remove MongoDB's internal ID
    return pd.DataFrame(data)
