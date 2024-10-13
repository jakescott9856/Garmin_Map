
def graphmain(User):
    import os
    import folium
    import pandas as pd

    # Filepaths to folders, list files and count files
    User_path = 'C:\\Users\\jaket\\Python Projects\\Garmin_Map\\' + str(User)
    CSV_path = os.path.join(User_path, 'CSV_files')
    CSV_filenames = [filename for filename in os.listdir(CSV_path) if os.path.isfile(os.path.join(CSV_path, filename))]
    num_files = str(len(CSV_filenames))
    num_current = 0

    # Find the last modified file
    last_modified_file = max(CSV_filenames, key=lambda x: os.path.getmtime(os.path.join(CSV_path, x)))

    # Create a map centered about lat long
    map_center = [52.1936, -2.7216]
    my_map = folium.Map(location=map_center, zoom_start=7)

    # Plot line for each file except the last modified file
    for fname in CSV_filenames:
        if fname != last_modified_file:
            num_current += 1
            print('Graphing: ' + User + ' ' + fname + ' (' + str(num_current) + '/' + num_files + ')')
            full_path = os.path.join(CSV_path, fname)
            points_df = pd.read_csv(full_path)
            df = points_df[['latitude', 'longitude']]

            line_color = 'blue'
            
            folium.PolyLine(
                locations=df[['latitude', 'longitude']].values,
                color=line_color,
            ).add_to(my_map)

    # Plot line for the last modified file
    full_path = os.path.join(CSV_path, last_modified_file)
    points_df = pd.read_csv(full_path)
    df = points_df[['latitude', 'longitude']]

    folium.PolyLine(
        locations=df[['latitude', 'longitude']].values,
        color='red',
    ).add_to(my_map)

    # Save the map to an HTML file
    print('')
    print('----- Saving Map -----')
    map_filepath = os.path.join(User_path, str(User) + "_map.html")
    my_map.save(map_filepath)
    print('')
    print('-------- Done --------')
    print('')