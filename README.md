# Mosam: Bangladesh Storm Risk Dashboard

A comprehensive web-based dashboard for assessing storm risk to health and education facilities in Bangladesh at the sub-district level.

## Features

- **Interactive Map**: Sub-district level visualization of Bangladesh with storm risk classification
- **Risk Assessment**: 5-level storm risk scoring based on Cyclone Amphan track and wind intensity
- **Facility Mapping**: 6,964 health facilities and 7,798 education facilities plotted
- **Hospital Density Analysis**: Classification of regions by healthcare facility density
- **Layer Controls**: Toggle visibility of storm track, health facilities, and education facilities
- **District Information**: Detailed popup information for each sub-district

## Installation

1. **Extract the files**:
   ```bash
   unzip bangladesh_storm_dashboard.zip
   cd bangladesh_storm_dashboard
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:5000`

## File Structure

```
bangladesh_storm_dashboard/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── processed_geodata.pkl           # Processed geospatial data
├── bangladesh_classified.geojson   # Classified district data
├── process_geojson.py             # Data processing script
├── analyze_data.py                # Risk analysis algorithms
├── templates/
│   └── index.html                 # Main dashboard template
└── static/
    ├── css/
    │   └── style.css              # Dashboard styling
    └── js/
        └── dashboard.js           # Interactive map functionality
```

## Data Sources

- **Administrative Boundaries**: Bangladesh sub-district polygons
- **Storm Track**: Cyclone Amphan 2020 track data with wind speeds
- **Health Facilities**: OpenStreetMap health facility points
- **Education Facilities**: OpenStreetMap education facility points

## Risk Classification

### Storm Risk Levels:
- **Level 5 (Very High)**: Wind speeds ≥120 mph - Red zones
- **Level 4 (High)**: Wind speeds 96-119 mph - Orange zones  
- **Level 3 (Medium)**: Wind speeds 74-95 mph - Yellow zones
- **Level 2 (Low)**: Wind speeds 39-73 mph - Light blue zones
- **Level 1 (Very Low)**: Wind speeds <39 mph - Blue zones
- **Level 0 (No Risk)**: Areas outside storm impact - Gray zones

### Hospital Density:
- **High**: Above 150% of mean facility count
- **Medium**: Above mean facility count
- **Low**: Below mean facility count

## Deployment

For production deployment, consider using:
- **Gunicorn** as WSGI server: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- **Nginx** as reverse proxy
- **Docker** for containerization

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Mapping**: Leaflet.js with OpenStreetMap tiles
- **Data Processing**: GeoPandas, Shapely
- **Spatial Analysis**: 50km buffer zones around storm track
- **Coordinate System**: WGS84 (EPSG:4326)

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## License

This project uses open data sources and is intended for disaster preparedness and emergency planning purposes.

