
import geopandas as gpd
import pandas as pd
import pickle
from shapely.geometry import Point

# Load processed GeoDataFrames
with open("processed_geodata.pkl", "rb") as f:
    data = pickle.load(f)

amphan_gdf = data["amphan_gdf"]
bangladesh_gdf = data["bangladesh_gdf"]
health_gdf = data["health_gdf"]
education_gdf = data["education_gdf"]

# Ensure all GeoDataFrames have a 'geometry' column and are valid
for gdf in [amphan_gdf, bangladesh_gdf, health_gdf, education_gdf]:
    if 'geometry' not in gdf.columns:
        print(f"Error: 'geometry' column not found in a GeoDataFrame.")
        exit()
    gdf = gdf[gdf.geometry.is_valid].copy()

# Spatial join to count health facilities per sub-district
health_facilities_per_district = gpd.sjoin(health_gdf, bangladesh_gdf, how="inner", predicate="intersects")
health_counts = health_facilities_per_district.groupby("NAME_4").size().reset_index(name="health_facility_count")
bangladesh_gdf = bangladesh_gdf.merge(health_counts, on="NAME_4", how="left")
bangladesh_gdf["health_facility_count"] = bangladesh_gdf["health_facility_count"].fillna(0).astype(int)

# Spatial join to count education facilities per sub-district
education_facilities_per_district = gpd.sjoin(education_gdf, bangladesh_gdf, how="inner", predicate="intersects")
education_counts = education_facilities_per_district.groupby("NAME_4").size().reset_index(name="education_facility_count")
bangladesh_gdf = bangladesh_gdf.merge(education_counts, on="NAME_4", how="left")
bangladesh_gdf["education_facility_count"] = bangladesh_gdf["education_facility_count"].fillna(0).astype(int)

# Calculate storm risk based on proximity to Amphan track and max_sustained_wind
# Define a buffer distance for storm impact (e.g., 50 km around the track)
# Reproject to a projected CRS for accurate buffering (e.g., UTM or a suitable local projection)
# For Bangladesh, a suitable UTM zone would be UTM Zone 45N (EPSG:32645)

bangladesh_utm = bangladesh_gdf.to_crs(epsg=32645)
amphan_utm = amphan_gdf.to_crs(epsg=32645)

# Create a buffer around the storm track. The buffer distance can be adjusted.
# Let's consider a 50km buffer for significant impact.
storm_buffer = amphan_utm.buffer(50000) # 50,000 meters = 50 km

# Dissolve the storm buffer to create a single polygon representing the total affected area
storm_affected_area = storm_buffer.unary_union

# Calculate storm severity for each sub-district
bangladesh_gdf["storm_risk_score"] = 0.0

for index, row in bangladesh_utm.iterrows():
    sub_district_geom = row.geometry
    if sub_district_geom.intersects(storm_affected_area):
        # If the sub-district intersects the storm affected area, calculate an average max_sustained_wind for the intersecting parts
        intersecting_amphan_points = amphan_utm[amphan_utm.intersects(sub_district_geom)]
        if not intersecting_amphan_points.empty:
            avg_wind = intersecting_amphan_points["max_sustained_wind"].mean()
            # Assign a risk score based on average wind speed (example logic)
            if avg_wind >= 120: # Category 3 hurricane equivalent
                bangladesh_gdf.loc[index, "storm_risk_score"] = 5 # Very High
            elif avg_wind >= 96: # Category 2
                bangladesh_gdf.loc[index, "storm_risk_score"] = 4 # High
            elif avg_wind >= 74: # Category 1
                bangladesh_gdf.loc[index, "storm_risk_score"] = 3 # Medium
            elif avg_wind >= 39: # Tropical Storm
                bangladesh_gdf.loc[index, "storm_risk_score"] = 2 # Low
            else:
                bangladesh_gdf.loc[index, "storm_risk_score"] = 1 # Very Low (Tropical Depression)

# Classify regions based on hospital density (example logic)
bangladesh_gdf["hospital_density_class"] = "Low"
median_health_facilities = bangladesh_gdf["health_facility_count"].median()
mean_health_facilities = bangladesh_gdf["health_facility_count"].mean()

bangladesh_gdf.loc[bangladesh_gdf["health_facility_count"] > mean_health_facilities, "hospital_density_class"] = "Medium"
bangladesh_gdf.loc[bangladesh_gdf["health_facility_count"] > (mean_health_facilities * 1.5), "hospital_density_class"] = "High"

# Save the updated GeoDataFrame with calculated metrics
bangladesh_gdf.to_file("bangladesh_classified.geojson", driver="GeoJSON")

print("Data analysis complete. Classified GeoJSON saved to bangladesh_classified.geojson")


