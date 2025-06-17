
import geopandas as gpd
import json

# Load GeoJSON files
with open('/home/ubuntu/upload/amphan_2020_track.geojson', 'r') as f:
    amphan_track = json.load(f)

with open('/home/ubuntu/upload/bangladesh.geojson', 'r') as f:
    bangladesh_districts = json.load(f)

with open('/home/ubuntu/upload/hotosm_bgd_health_facilities_points_geojson.geojson', 'r') as f:
    health_facilities = json.load(f)

with open('/home/ubuntu/upload/hotosm_bgd_education_facilities_points_geojson.geojson', 'r') as f:
    education_facilities = json.load(f)

# Convert to GeoDataFrames
amphan_gdf = gpd.GeoDataFrame.from_features(amphan_track['features'])
bangladesh_gdf = gpd.GeoDataFrame.from_features(bangladesh_districts['features'])
health_gdf = gpd.GeoDataFrame.from_features(health_facilities['features'])
education_gdf = gpd.GeoDataFrame.from_features(education_facilities['features'])

# Set CRS for all GeoDataFrames to WGS84 (EPSG:4326) if not already set or if it's different
# The aoi_bangladesh.geojson is in EPSG:3857, but the others seem to be in WGS84 based on coordinate values.
# We'll reproject everything to EPSG:4326 for consistency and easier spatial operations.

# Check and set CRS for amphan_gdf
if amphan_gdf.crs is None:
    amphan_gdf.crs = 'EPSG:4326'
else:
    amphan_gdf = amphan_gdf.to_crs('EPSG:4326')

# Check and set CRS for bangladesh_gdf
if bangladesh_gdf.crs is None:
    bangladesh_gdf.crs = 'EPSG:4326'
else:
    bangladesh_gdf = bangladesh_gdf.to_crs('EPSG:4326')

# Check and set CRS for health_gdf
if health_gdf.crs is None:
    health_gdf.crs = 'EPSG:4326'
else:
    health_gdf = health_gdf.to_crs('EPSG:4326')

# Check and set CRS for education_gdf
if education_gdf.crs is None:
    education_gdf.crs = 'EPSG:4326'
else:
    education_gdf = education_gdf.to_crs('EPSG:4326')

# Display basic info about each GeoDataFrame
print('Amphan Track GeoDataFrame Info:')
print(amphan_gdf.info())
print('\nAmphan Track GeoDataFrame Head:')
print(amphan_gdf.head())

print('\nBangladesh Districts GeoDataFrame Info:')
print(bangladesh_gdf.info())
print('\nBangladesh Districts GeoDataFrame Head:')
print(bangladesh_gdf.head())

print('\nHealth Facilities GeoDataFrame Info:')
print(health_gdf.info())
print('\nHealth Facilities GeoDataFrame Head:')
print(health_gdf.head())

print('\nEducation Facilities GeoDataFrame Info:')
print(education_gdf.info())
print('\nEducation Facilities GeoDataFrame Head:')
print(education_gdf.head())

# Save processed dataframes to a pickle file for later use
import pickle
with open('processed_geodata.pkl', 'wb') as f:
    pickle.dump({
        'amphan_gdf': amphan_gdf,
        'bangladesh_gdf': bangladesh_gdf,
        'health_gdf': health_gdf,
        'education_gdf': education_gdf
    }, f)

print('\nAll GeoJSON files loaded and converted to GeoDataFrames. CRS set to EPSG:4326. Data saved to processed_geodata.pkl')


