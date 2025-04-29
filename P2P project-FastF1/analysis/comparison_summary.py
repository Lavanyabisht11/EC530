import pandas as pd

def generate_driver_summary():
    # Load laps from received CSV
    laps = pd.read_csv('../2023_Italian_Grand_Prix_laps.csv')
    
    # Convert LapTime to seconds
    laps['LapTimeSeconds'] = pd.to_timedelta(laps['LapTime']).dt.total_seconds()
    
    # Number of laps completed
    lap_counts = laps.groupby('Driver')['LapNumber'].count()
    
    # Average and Fastest lap times
    avg_laptimes = laps.groupby('Driver')['LapTimeSeconds'].mean()
    fastest_laps = laps.groupby('Driver')['LapTimeSeconds'].min()
    
    # Standard deviation (consistency)
    lap_std = laps.groupby('Driver')['LapTimeSeconds'].std()
    
    # First half vs Second half performance
    max_lap = laps['LapNumber'].max()
    laps['Half'] = laps['LapNumber'] > (max_lap / 2)
    half_pace = laps.groupby(['Driver', 'Half'])['LapTimeSeconds'].mean().unstack()
    
    # Combine into a single table
    summary = pd.DataFrame({
        'LapsCompleted': lap_counts,
        'AvgLapTime(s)': avg_laptimes,
        'FastestLap(s)': fastest_laps,
        'StdDevLapTime(s)': lap_std,
        'FirstHalfAvg(s)': half_pace[False],  # False → first half
        'SecondHalfAvg(s)': half_pace[True],  # True → second half
    })
    
    # Save as CSV
    summary = summary.round(3)  # Round for nice output
    summary = summary.sort_values('AvgLapTime(s)')  # Sort by average lap time
    summary.to_csv('driver_summary.csv')
    
    # Print nicely
    print("\nDriver Summary Table:")
    print(summary)

if __name__ == "__main__":
    generate_driver_summary()
