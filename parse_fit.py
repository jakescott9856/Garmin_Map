def main(User):
    # Imports
    import os
    from datetime import datetime, timedelta
    from typing import Dict, Union, Optional, Tuple
    import pandas as pd
    import fitdecode

    POINTS_COLUMN_NAMES = ['latitude', 'longitude', 'lap', 'altitude', 'timestamp', 'heart_rate', 'cadence', 'speed']
    LAPS_COLUMN_NAMES = ['number', 'start_time', 'total_distance', 'total_elapsed_time',
                         'max_speed', 'max_heart_rate', 'avg_heart_rate']

    def get_fit_lap_data(frame):
        data = {}
        for field in LAPS_COLUMN_NAMES[1:]:
            if frame.has_field(field):
                data[field] = frame.get_value(field)
        return data

    def get_fit_point_data(frame):
        data = {}
        if not (frame.has_field('position_lat') and frame.has_field('position_long')):
            return None
        data['latitude'] = frame.get_value('position_lat') / ((2**32) / 360)
        data['longitude'] = frame.get_value('position_long') / ((2**32) / 360)
        for field in POINTS_COLUMN_NAMES[4:]:  # Skip 'activity_type', 'latitude', 'longitude', 'lap'
            if frame.has_field(field):
                data[field] = frame.get_value(field)
        return data

    def get_dataframes(fname: str) -> Tuple[pd.DataFrame, pd.DataFrame, str]:
        points_data = []
        laps_data = []
        lap_no = 1
        activity_type = 'unknown'
        with fitdecode.FitReader(fname) as fit_file:
            for frame in fit_file:
                if isinstance(frame, fitdecode.records.FitDataMessage):
                    if frame.name == 'sport' and frame.has_field('sport'):
                        activity_type = str(frame.get_value('sport'))
                    elif frame.name == 'session' and frame.has_field('sport'):
                        activity_type = str(frame.get_value('sport'))

        with fitdecode.FitReader(fname) as fit_file:
            for frame in fit_file:
                if isinstance(frame, fitdecode.records.FitDataMessage):
                    if frame.name == 'sport' and frame.has_field('sport'):
                        activity_type = str(frame.get_value('sport'))
                    elif frame.name == 'lap':
                        single_lap_data = get_fit_lap_data(frame)
                        single_lap_data['number'] = lap_no
                        laps_data.append(single_lap_data)
                        lap_no += 1
                    elif frame.name == 'record':
                        single_point_data = get_fit_point_data(frame)
                        if single_point_data is not None:
                            single_point_data['lap'] = lap_no
                            points_data.append(single_point_data)

        # Add activity_type to each point
        for point in points_data:
            point['activity_type'] = activity_type

        laps_df = pd.DataFrame(laps_data, columns=LAPS_COLUMN_NAMES)
        laps_df.set_index('number', inplace=True)
        points_df = pd.DataFrame(points_data, columns=POINTS_COLUMN_NAMES)

        return laps_df, points_df, activity_type

    def csv_file_exists(csv_filepath):
        return os.path.isfile(csv_filepath)

    # Filepaths
    FIT_path = f'C:\\Users\\jaket\\Python Projects\\Garmin_Map\\{User}\\FIT_files'
    CSV_path = f'C:\\Users\\jaket\\Python Projects\\Garmin_Map\\{User}\\CSV_files'

    FIT_filenames = [filename for filename in os.listdir(FIT_path)
                     if os.path.isfile(os.path.join(FIT_path, filename))]
    num_files = str(len(FIT_filenames))
    num_current = 0

    for fname in FIT_filenames:
        num_current += 1
        full_path = os.path.join(FIT_path, fname)
        csv_filename = f'{os.path.splitext(fname)[0]}.csv'
        csv_filepath = os.path.join(CSV_path, csv_filename)

        if csv_file_exists(csv_filepath):
            print(f'Skipping {csv_filename} - CSV file already exists. ({num_current}/{num_files})')
        else:
            print(f'Working on: {User} {fname} ({num_current}/{num_files})')
            laps_df, points_df, activity_type = get_dataframes(full_path)

            with open(csv_filepath, 'w', newline='') as f:
                f.write(f'Activity Type:,{activity_type}\n')
                points_df.to_csv(f, index=False)

    print('\n-------- Done --------\n')