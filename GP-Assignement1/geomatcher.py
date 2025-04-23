import math
from typing import List, Tuple

# Radius of Earth in kilometers
EARTH_RADIUS_KM = 6371.0

def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculates the great-circle distance between two points on the Earth using the Haversine formula.
    
    Args:
        coord1: Tuple containing (latitude, longitude) of point A in degrees.
        coord2: Tuple containing (latitude, longitude) of point B in degrees.
    
    Returns:
        Distance in kilometers.
    """
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    return EARTH_RADIUS_KM * c


def match_closest_points(source: List[Tuple[float, float]], targets: List[Tuple[float, float]]) -> List[Tuple[Tuple[float, float], Tuple[float, float], float]]:
    """
    Matches each point in the source list to its nearest point in the target list.
    
    Args:
        source: List of (lat, lon) tuples representing source locations.
        targets: List of (lat, lon) tuples representing target locations.
    
    Returns:
        List of tuples: (source_point, closest_target_point, distance_km)
    """
    matches = []

    for src in source:
        closest = min(targets, key=lambda tgt: haversine_distance(src, tgt))
        distance = haversine_distance(src, closest)
        matches.append((src, closest, distance))

    return matches
