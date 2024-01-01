import folium
from shapely.geometry import LineString, Point
import geopandas as gpd
from geopy.geocoders import Nominatim

def find_path_between_ports(port1, port2, world):
    # Create LineString from the two ports
    line = LineString([Point(port1[::-1]), Point(port2[::-1])])

    # Initialize the new_line with the original line
    new_line = line

    # Iterate until there are no more intersections
    while True:
        # Find the intersection with land polygons
        intersection = world.unary_union.intersection(new_line)

        # If the intersection is empty, break the loop
        if intersection.is_empty:
            break

        # Create a new LineString avoiding land
        new_line = new_line.difference(intersection)
        print(new_line)
    # Extract coordinates directly from the final LineString
    new_line_coords = list(new_line.coords)

    # Ensure the coordinates are in the correct order
    new_line_coords = [(coord[1], coord[0]) for coord in new_line_coords]

    return new_line_coords

def draw_yacht_tracks(port1, port2, world):
    # Create a Folium map centered between the two ports
    map_center = [(port1[0] + port2[0]) / 2, (port1[1] + port2[1]) / 2]
    yacht_map = folium.Map(location=map_center, zoom_start=5)

    # Add markers for the two ports
    folium.Marker(port1, popup='Port 1').add_to(yacht_map)
    folium.Marker(port2, popup='Port 2').add_to(yacht_map)

    # Find a path avoiding land
    yacht_tracks = find_path_between_ports(port1, port2, world)

    # Draw yacht tracks using the PolyLine plugin
    folium.PolyLine(yacht_tracks, color='blue', weight=2.5, opacity=1).add_to(yacht_map)

    # Display the map
    yacht_map.save('yacht_tracks_map.html')

# Example coordinates for two ports (replace with actual coordinates)
port1_coords = [48.26947, -4.82112]  
port2_coords = [51.44513, -5.34]  

# Load world shapefile (you can download it from Natural Earth: https://www.naturalearthdata.com/downloads/110m-physical-vectors/)
world = gpd.read_file('ne_110m_land/ne_110m_land.shp')

# Draw yacht tracks between the two ports avoiding land
draw_yacht_tracks(port1_coords, port2_coords, world)

