import overpy
import json

api = overpy.Overpass()

city_name = 'Berlin'

query = """
[out:json];
area
    ["boundary"="administrative"]
    ["name"="{}"]->.a;          // Redirect result to ".a"
out body qt;
(
    node
        (area.a)                    // Use result from ".a"
        ["amenity"~"fast_food|restaurant"];
    way
        (area.a)                    // Use again result from ".a"
        ["amenity"~"fast_food|restaurant"];
);
out body qt;
>;
out skel qt;
"""

result = api.query(query.format(city_name))

# transform data
result = [(node.tags, float(node.lat), float(node.lon)) for node in result.nodes]

amenities = []
for node in result:
    tags, lat, lon = node
    tags.update({'lat':lat,
                 'lon': lon})
    amenities.append(tags)

with open(f'data/raw_data_{city_name}.json', 'w') as outfile:
    json.dump(amenities, outfile)
