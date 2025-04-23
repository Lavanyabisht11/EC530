from geo_matcher import match_closest_points

# Example coordinates (latitude, longitude)
source_points = [(42.3601, -71.0589), (34.0522, -118.2437)]  # Boston, LA
target_points = [(40.7128, -74.0060), (37.7749, -122.4194)]  # NYC, SF

matches = match_closest_points(source_points, target_points)

for src, tgt, dist in matches:
    print(f"Source: {src} -> Closest Target: {tgt} | Distance: {dist:.2f} km")
