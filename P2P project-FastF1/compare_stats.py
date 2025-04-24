import matplotlib.pyplot as plt
from db.db_handler import load_laps_from_mongo

def plot_lap_time_comparison(driver1_code: str, driver2_code: str):
    df1 = load_laps_from_mongo(driver1_code)
    df2 = load_laps_from_mongo(driver2_code)

    # Convert lap times to seconds (FastF1 gives timedelta64)
    df1['LapTimeSeconds'] = df1['LapTime'].dt.total_seconds()
    df2['LapTimeSeconds'] = df2['LapTime'].dt.total_seconds()

    plt.figure(figsize=(10, 5))
    plt.plot(df1['LapNumber'], df1['LapTimeSeconds'], label=driver1_code, marker='o')
    plt.plot(df2['LapNumber'], df2['LapTimeSeconds'], label=driver2_code, marker='x')

    plt.title("Lap Time Comparison")
    plt.xlabel("Lap Number")
    plt.ylabel("Lap Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_lap_time_comparison("LEC", "PEER")
