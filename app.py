from flask import Flask, render_template, jsonify
import geopandas as gpd
import json
import pickle

app = Flask(__name__)

# Load processed data
with open("processed_geodata.pkl", "rb") as f:
    data = pickle.load(f)

amphan_gdf = data["amphan_gdf"]
health_gdf = data["health_gdf"]
education_gdf = data["education_gdf"]

# Load classified Bangladesh data
bangladesh_classified = gpd.read_file("bangladesh_classified.geojson")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bangladesh')
def get_bangladesh_data():
    # Convert to GeoJSON format for frontend
    return jsonify(json.loads(bangladesh_classified.to_json()))

@app.route('/api/amphan')
def get_amphan_data():
    # Convert to GeoJSON format for frontend
    return jsonify(json.loads(amphan_gdf.to_json()))

@app.route('/api/health')
def get_health_data():
    # Convert to GeoJSON format for frontend
    return jsonify(json.loads(health_gdf.to_json()))

@app.route('/api/education')
def get_education_data():
    # Convert to GeoJSON format for frontend
    return jsonify(json.loads(education_gdf.to_json()))

@app.route('/api/stats')
def get_stats():
    # Calculate summary statistics
    total_districts = len(bangladesh_classified)
    high_risk_districts = len(bangladesh_classified[bangladesh_classified['storm_risk_score'] >= 4])
    high_density_hospitals = len(bangladesh_classified[bangladesh_classified['hospital_density_class'] == 'High'])
    total_health_facilities = len(health_gdf)
    total_education_facilities = len(education_gdf)
    
    return jsonify({
        'total_districts': total_districts,
        'high_risk_districts': high_risk_districts,
        'high_density_hospitals': high_density_hospitals,
        'total_health_facilities': total_health_facilities,
        'total_education_facilities': total_education_facilities
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

