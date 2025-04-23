from geo_matcher import match_closest_points

# Example data
source_points = [(42.3601, -71.0589), (34.0522, -118.2437)]  # Boston, LA
target_points = [(40.7128, -74.0060), (37.7749, -122.4194)]  # NYC, SF

results = match_closest_points(source_points, target_points)

for src, tgt, dist in results:
    print(f"Source: {src} -> Closest Target: {tgt} | Distance: {dist:.2f} km")
