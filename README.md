# Cell Tower Location Tracking using OpenCellID & Google Maps API

## Overview
This project retrieves the latitude and longitude of cell towers using the OpenCellID API and maps their locations on Google Maps. It also plots the approximate path followed by a user based on cell tower locations using the Google Routes API.
![Screenshot at 2025-03-16 00-37-03](https://github.com/user-attachments/assets/85fa1ab5-7eee-4de4-bd71-0d0aacd5145e)

## Features
- Retrieves cell tower locations from OpenCellID API.
- Plots them on map using Folium.
- Uses Google Maps API to generate possible movement routes.
- Outputs map results as an HTML file.

## Setup Instructions
### 1️ Get API Keys
#### OpenCellID API Key:
1. Register at [OpenCellID](https://opencellid.org/).
2. Verify your email then log in.
3. Navigate to the Access Token section and copy your key.
![image](https://github.com/user-attachments/assets/91f4b905-bd8e-4307-8470-696bf12835ff)

#### Google API Key:
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the **Routes API**.
4. Generate an API Key under **Credentials**.
5. Restrict API usage to prevent unauthorized access. (I am currently using it unrestricted)
![Screenshot at 2025-03-16 00-55-51](https://github.com/user-attachments/assets/dbb4fd05-a404-4fe5-9671-2681e9793e50)
![Screenshot at 2025-03-16 00-57-03](https://github.com/user-attachments/assets/4b343bff-bf1d-45e3-9d81-89b8e8088f6e)

### 2️ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️ Prepare Data
Store cell tower data in `.csv` with the following structure:
opencellid provides data for towers also.
```csv
ID,time stamp,MCC,MNC,LAC,CellID
,,648,3,112,20046
,,648,3,108,10013
```
In the current implimentation `time stamp` is of no use but can be levaraged later...

For getting the MCC, MNC, LAC and CellID for your device you can download Android applications `Signal Detector`.
![image](https://github.com/user-attachments/assets/d80c83b8-d737-4335-ad85-aa234c851512)
![image](https://github.com/user-attachments/assets/98fe73da-342a-414c-91ef-576dd856dfe4)

### 4️ Run the Script
```sh
python cell_mapper.py
```

## How Governments Use Advanced Versions
Many governments and telecom providers use advanced versions of this system for:
- **Surveillance & Security**: Tracking movements of persons of interest.
- **Emergency Services**: Locating users in distress when GPS is unavailable.
- **Triangulation**: Used to track approximate location of cell user/suspect.

## Limitations
- **Limited Data Availability**: OpenCellID is crowdsourced, making incomplete coverage.
- **No Real-Time Tracking**: The system relies on pre-stored tower locations.
- **Restricted in Some Countries**: In many countries including India, this data is either very old or not available (for this project i used Zimbabwe).
- **Accuracy Issues**: Location precision depends on the density of towers in an area.

## Future Improvements
- Use real-time telecom APIs (if available) for better accuracy.
- Implement machine learning models to predict user paths.
- Improve visualization using web-based interactive dashboards.


