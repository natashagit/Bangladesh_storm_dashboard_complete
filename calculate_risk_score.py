import geopandas as gpd
import pandas as pd


def calculate_comprehensive_risk():
    print("Loading data...")
    # Load the classified data
    bangladesh_gdf = gpd.read_file(
        "bangladesh_classified_with_children.geojson"
    )
    
    # Calculate percentiles for health facilities and children population
    health_p25 = bangladesh_gdf['health_facility_count'].quantile(0.25)
    health_p75 = bangladesh_gdf['health_facility_count'].quantile(0.75)
    children_p25 = bangladesh_gdf['children_under_five'].quantile(0.25)
    children_p75 = bangladesh_gdf['children_under_five'].quantile(0.75)
    
    print("Calculating risk scores...")
    # Initialize risk score
    bangladesh_gdf['storm_risk_score'] = 0
    
    # Calculate health facility risk (inverse relationship)
    # Lower number of facilities = higher risk
    bangladesh_gdf['health_risk'] = pd.cut(
        bangladesh_gdf['health_facility_count'],
        bins=[-float('inf'), health_p25, health_p75, float('inf')],
        labels=[3, 2, 1],  # 3 = high risk (few facilities), 1 = low risk
        include_lowest=True
    ).astype(int)
    
    # Calculate children population risk
    # Higher number of children = higher risk
    bangladesh_gdf['children_risk'] = pd.cut(
        bangladesh_gdf['children_under_five'],
        bins=[-float('inf'), children_p25, children_p75, float('inf')],
        labels=[1, 2, 3],  # 3 = high risk (many children), 1 = low risk
        include_lowest=True
    ).astype(int)
    
    # Calculate distance risk
    distance_risk_map = {
        'Very Close': 3,
        'Close': 2,
        'Moderate': 1,
        'Far': 0
    }
    bangladesh_gdf['distance_risk'] = (
        bangladesh_gdf['storm_distance_class'].map(distance_risk_map)
    )
    
    # Calculate comprehensive risk score
    # Weights: distance (50%), health facilities (25%), children (25%)
    bangladesh_gdf['storm_risk_score'] = (
        bangladesh_gdf['distance_risk'] * 0.5 +
        bangladesh_gdf['health_risk'] * 0.25 +
        bangladesh_gdf['children_risk'] * 0.25
    )
    
    # Scale to 0-5 range
    max_score = bangladesh_gdf['storm_risk_score'].max()
    bangladesh_gdf['storm_risk_score'] = (
        (bangladesh_gdf['storm_risk_score'] / max_score) * 5
    ).round()
    
    # Add risk level labels
    risk_labels = {
        5: 'Very High',
        4: 'High',
        3: 'Medium',
        2: 'Low',
        1: 'Very Low',
        0: 'No Risk'
    }
    bangladesh_gdf['risk_level'] = bangladesh_gdf['storm_risk_score'].map(risk_labels)
    
    print("Saving results...")
    # Save the updated GeoJSON
    bangladesh_gdf.to_file(
        "bangladesh_classified_with_children.geojson",
        driver="GeoJSON"
    )
    
    # Print summary statistics
    print("\nRisk Score Distribution:")
    print(bangladesh_gdf['storm_risk_score'].value_counts().sort_index())
    
    print("\nRisk Level Distribution:")
    print(bangladesh_gdf['risk_level'].value_counts())
    
    print("\nTop 5 Highest Risk Districts:")
    cols = [
        'NAME_4', 'storm_risk_score', 'risk_level',
        'health_facility_count', 'children_under_five',
        'storm_distance_class'
    ]
    print(
        bangladesh_gdf[cols]
        .sort_values('storm_risk_score', ascending=False)
        .head()
    )


if __name__ == "__main__":
    calculate_comprehensive_risk() 