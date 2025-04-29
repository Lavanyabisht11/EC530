import pandas as pd
import matplotlib.pyplot as plt

def plot_lap_time_comparison(driver1_code: str, driver2_code: str):
    # Load laps from CSV
    laps = pd.read_csv('../2023_Italian_Grand_Prix_laps.csv')  # Correct path from 'analysis' folder

    # Convert LapTime to seconds
    laps['LapTimeSeconds'] = pd.to_timedelta(laps['LapTime']).dt.total_seconds()

    # Separate data for driver1 and driver2
    df1 = laps[laps['Driver'] == driver1_code]
    df2 = laps[laps['Driver'] == driver2_code]

    plt.figure(figsize=(10, 5))
    plt.plot(df1['LapNumber'], df1['LapTimeSeconds'], label=driver1_code, marker='o')
    plt.plot(df2['LapNumber'], df2['LapTimeSeconds'], label=driver2_code, marker='x')

    plt.title(f"Lap Time Comparison: {driver1_code} vs {driver2_code}")
    plt.xlabel("Lap Number")
    plt.ylabel("Lap Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_lap_time_comparison("HAM", "VER")  # You can change drivers as needed
