import os
import folium
import pandas as pd

CSV_path = 'C:\\Users\\jaket\\Python Projects\\Garmin_Map\\CSV_files'
CSV_filenames = [filename for filename in os.listdir(CSV_path) if os.path.isfile(os.path.join(CSV_path, filename))]
num_files = str(len(CSV_filenames))
num_current = 0

# Create a map centered around the first point
map_center = [51.8017, -4.9691]
my_map = folium.Map(location=map_center, zoom_start=10)

for fname in CSV_filenames:
    num_current += 1
    print('Working on: '+ fname + ' ('+str(num_current)+'/'+num_files+')')
    full_path = os.path.join(CSV_path, fname)
    points_df = pd.read_csv(full_path)
    df = points_df[['latitude', 'longitude']]
    folium.PolyLine(locations=df[['latitude', 'longitude']].values, color='blue').add_to(my_map)

# Save the map to an HTML file
print('')
print('----- Saving Map -----')
my_map.save("Garmin_Map.html")
print('')
print('-------- Done --------')
print('')