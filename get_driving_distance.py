import pandas as pd
import requests
import json


# Method for calling the API
def call_matrix_api(origins, destinations):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    key = ''  # INSERT API KEY !!!
    params = {'key': key, 'origins': origins, 'destinations': destinations}

    req = requests.get(url=url, params=params)
    response = json.loads(req.content)
    return response


# Read the location data
df = pd.read_excel('Book1.xlsx')

# Get the list of destinations
destinations = df['destination'].value_counts().index

results = []
count_calls = 0
for destination in destinations:
    # Leave only rows with one destination
    df_temp = df[df['destination'] == destination]
    df_temp = df_temp.reset_index()

    origins = ''
    origins_aray = []
    counter = 0

    # Put origins into right format: single string with | as separator
    for location in df_temp['origin']:
        # Each string has at most 25 origins, in case of more create a list of strings
        if counter > 24:
            origins_aray.append(origins)
            origins = ''
            counter = 0

        origins += location + '|'
        counter += 1

    origins_aray.append(origins)

    distances = []
    times = []

    # For each string of origins, call the API
    for origins_string in origins_aray:
        api_response = call_matrix_api(origins_string, destination)
        count_calls += 1

        # Extract driving distance and time
        if api_response['status'] == 'OK':
            for row in api_response['rows']:
                for element in row['elements']:
                    if element['status'] == 'OK':
                        distances.append(element['distance']['value'])
                        times.append(element['duration']['value'])
                    else:
                        distances.append(-1)
                        times.append(-1)

    # Create result rows and append to the results list
    for i in range(len(distances)):
        results.append([df_temp['origin'][i], destination, distances[i], times[i]])

# Create a dataframe out of the results list
results_df = pd.DataFrame(results, columns=['origin', 'destination', 'driving distance [m]', 'driving time [s]'])

# Export to CSV / Excel
results_df.to_csv('driving-distances.csv')
results_df.to_excel('driving-distances.xlsx')
