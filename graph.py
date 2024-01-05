import os
import folium
import pandas as pd

User = 'JS'
User_path = 'C:\\Users\\jaket\\Python Projects\\Garmin_Map\\'+ str(User)
CSV_path = 'C:\\Users\\jaket\\Python Projects\\Garmin_Map\\'+ str(User)+'\\CSV_files'
CSV_filenames = [filename for filename in os.listdir(CSV_path) if os.path.isfile(os.path.join(CSV_path, filename))]
num_files = str(len(CSV_filenames))
num_current = 0

# Create a map centered around the first point
map_center = [52.1936, -2.7216]
my_map = folium.Map(location=map_center, zoom_start=7)

#color_list = ['blue', 'red', 'green', 'purple']

for fname in CSV_filenames:
    num_current += 1
    #col = num_current % len(color_list)
    print('Working on: '+User +' '+ fname + ' ('+str(num_current)+'/'+num_files+')' )
    full_path = os.path.join(CSV_path, fname)
    points_df = pd.read_csv(full_path)
    df = points_df[['latitude', 'longitude']]
    folium.PolyLine(locations=df[['latitude', 'longitude']].values, \
        color='blue',opacity=1).add_to(my_map)

# Save the map to an HTML file
print('')
print('----- Saving Map -----')
map_filepath = os.path.join(User_path, str(User)+"_map.html")
my_map.save(map_filepath)
print('')
print('-------- Done --------')
print('')