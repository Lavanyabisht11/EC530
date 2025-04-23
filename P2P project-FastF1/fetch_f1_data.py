import fastf1
import pandas as pd

def fetch_race_data(year: int, gp_name: str, session_type: str = 'R') -> pd.DataFrame:
    """
    Fetches lap-by-lap data from a specified F1 session using FastF1.

    Args:
        year: The season year (e.g. 2023)
        gp_name: Grand Prix name (e.g. "Italian Grand Prix")
        session_type: Session type (e.g. 'R' for Race, 'Q' for Qualifying)

    Returns:
        A DataFrame of all laps from all drivers.
    """
    fastf1.Cache.enable_cache('./cache')  # Enables caching in a folder
    session = fastf1.get_session(year, gp_name, session_type)
    session.load()
    
    laps = session.laps
    print(f"Loaded {len(laps)} laps for {gp_name} {session_type.upper()} {year}")
    return laps

if __name__ == "__main__":
    # Example: Italian Grand Prix 2023
    year = 2023
    gp = "Italian Grand Prix"
    laps_df = fetch_race_data(year, gp)
    
    # Optional: Save to CSV for debugging
    laps_df.to_csv(f"{year}_{gp.replace(' ', '_')}_laps.csv", index=False)
    print("Lap data saved to CSV.")
