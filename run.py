from flask import Flask, render_template
import folium
import csv
import itertools

app = Flask(__name__)


def crime_icon(crime):
    if crime and 'theft' in crime.lower():
        return folium.Icon(color='red', icon='usd')
    else:
        return folium.Icon(color='blue', icon='exclamation-sign')


@app.route('/')
def home():
    start_coords = (51.514203, -0.094628)
    fmap = folium.Map(location=start_coords,
                      tiles='OpenStreetMap', zoom_start=10)

    with open('data.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        for row in reader:
            latitude, longitude = row['Latitude'], row['Longitude']
            if latitude and longitude:
                crime_type = row.get('Crime type')
                latitude, longitude = float(latitude), float(longitude)

                try:
                    folium.Marker((latitude, longitude), popup=crime_type,
                                  icon=crime_icon(crime_type)).add_to(fmap)
                except Exception as e:
                    print(e)

    fmap.save(outfile='templates/crime_map.html')
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
