import json
import folium   # map making
import polyline  # decoding google polyline for map making
import requests
import pandas as pd
import xml.etree.ElementTree as ET # for getting data from opencellid api

csv_file = 'celldata2.csv'   # path to your csv file

OPENCELL_URL = "https://opencellid.org/cell/get?key={key}&mcc={mcc}&mnc={mnc}&lac={lac}&cellid={cellid}"
OPENCELL_API_KEY = ""        # enter your open cell id API key
GOOGLE_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
GOOGLE_API_KEY = ''      # enter your google console API key

locations = []

def get_cell_location(OPENCELL_API_KEY, MCC, MNC, LAC, CellID):

    url = OPENCELL_URL.format(key = OPENCELL_API_KEY, mcc = MCC, mnc = MNC, lac = LAC, cellid = CellID)
    response = requests.get(url)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            if root.attrib.get('stat') == 'ok':
                lat = root.find('cell').attrib.get('lat')
                lon = root.find('cell').attrib.get('lon')
                if lat and lon:
                    locations.append((float(lat), float(lon))) 
                    return float(lat), float(lon)
        except ET.ParseError:
            return None
    return None

def plot_cells_on_map(csv_file, OPENCELL_API_KEY):
    df = pd.read_csv(csv_file)

    for _, row in df.iterrows():
        mcc = int(row['MCC'])
        mnc = int(row['MNC'])
        lac = int(row['LAC'])
        cellid = int(row['CellID'])

        get_cell_location(OPENCELL_API_KEY, mcc, mnc, lac, cellid)

def get_directions():
    if len(locations) < 2:
        print("More than 2 points are nneded to get directions.....")
        return none
    
    start_latitude, start_longitude = locations[0]
    dest_latitude, dest_longitude = locations[-1]

    waypoints = [
        {"location": {"latLng": {"latitude": lat, "longitude": lon}}}
        for lat, lon in locations[1:-1]
    ]
    data = {
        "origin": {
            "location": {"latLng": {"latitude": start_latitude, "longitude": start_longitude}}
        },
        "destination": {
            "location": {"latLng": {"latitude": dest_latitude, "longitude": dest_longitude}}
        },
        "intermediates": waypoints,
        "travelMode": "DRIVE"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "routes.polyline.encodedPolyline"
    }

    response = requests.post(GOOGLE_URL, headers = headers, data = json.dumps(data))

    if response.status_code == 200:
        route_data = response.json()
        if "routes" in route_data and len(route_data["routes"]) > 0:
            return route_data["routes"][0]["polyline"]["encodedPolyline"]
        else:
            print("Routes not found!")
            return None
    else:
        print("Error getting the directions:", response.text)
        return None

def plot_route_on_map():
    if not locations:
        print("Can not plot: No locations to plot...")
        return
    
    m = folium.Map(location=locations[0], zoom_start=12)

    encoded_polyline = get_directions()
    
    if encoded_polyline:
        decoded_route = polyline.decode(encoded_polyline)
        folium.PolyLine(decoded_route, color="green", weight=3, opacity=0.7).add_to(m)

        folium.Marker(locations[0], popup=f"Start: lon:{locations[0][1]}, lat:{locations[0][0]}", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(locations[-1], popup=f"End: lon:{locations[-1][1]}, lat:{locations[-1][0]}", icon=folium.Icon(color="red")).add_to(m)

        m.save("route_map.html")
        print("Route map saved as route_map.html")
    else:
        print("Failed to plot route.")


plot_cells_on_map(csv_file, OPENCELL_API_KEY)
plot_route_on_map()
