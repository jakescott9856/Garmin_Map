
def main(User,Map_display,Red_modified):
    import os
    import folium
    import pandas as pd
    from datetime import datetime

    Red_modified_date = datetime.strptime(Red_modified, '%d/%m/%Y')

    # Filepaths to folders, list files and count files
    User_path = 'C:\\Users\\jaket\\Python Projects\\Garmin_Map\\' + str(User)
    CSV_path = os.path.join(User_path, 'CSV_files')
    CSV_filenames = [filename for filename in os.listdir(CSV_path) if os.path.isfile(os.path.join(CSV_path, filename))]
    num_files = str(len(CSV_filenames))
    num_current = 0

    

    # Create a map centered about lat long
    map_center = [52.1936, -2.7216]
    my_map = folium.Map(location=map_center, zoom_start=7)
    unknown_activity_list = []
    # Helper function to extract lat/lon from file
    def extract_latlon(filepath):
        # Read only the point data (after 3 metadata lines + 1 blank line)
        return pd.read_csv(filepath, skiprows=1)[['latitude', 'longitude']]

    # Plot line for each file except the last modified file
    for fname in CSV_filenames:
        num_current += 1
        print('Graphing: ' + User + ' ' + fname + ' (' + str(num_current) + '/' + num_files + ')')
        full_path = os.path.join(CSV_path, fname)
        mod_time = datetime.fromtimestamp(os.path.getmtime(full_path))
        # Optional: read and display metadata
        metadata = pd.read_csv(full_path, nrows=1, header=None)
        activity = metadata.iloc[0,1].lower() if metadata.shape[1] > 1 else ''
       
        df = extract_latlon(full_path)
        if mod_time > Red_modified_date:
            line_color = 'red'
        else:
            if 'cycling' in activity:
                line_color = 'blue'
            elif 'sailing' in activity or 'kayaking' in activity or 'boating' in activity or 'rowing' in activity:
                line_color = 'white'
            elif 'running' in activity or 'walking' in activity or 'hiking' in activity:
                line_color = 'green'
            elif 'swimming' in activity:
                line_color = 'purple'
            else:
                line_color = 'black'
                unknown_activity_list.append(full_path)
        
        if Map_display == 'Cycling':
            if 'cycling' in activity:
                folium.PolyLine(locations=df.values,color=line_color,).add_to(my_map)

        if Map_display == 'All':
            folium.PolyLine(locations=df.values,color=line_color,).add_to(my_map)

    # Save the map to an HTML file
    print(unknown_activity_list)
    print('')
    print('----- Saving Map -----')
    map_filepath = os.path.join(User_path, str(User) + "_map.html")
    my_map.save(map_filepath)
    print('')
    print('-------- Done --------')
    print('')