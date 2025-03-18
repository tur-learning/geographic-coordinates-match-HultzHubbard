from utils import extract_files, load_data, save_to_json, print_dict, find_closest_matches, convert_to_geojson
###############################
# 1) Define the input files
###############################
# HINT: The goal is to analyze the previously non-matched Nolli entries
#       from the previous assignment and try to match them using a different approach.
#
# You will load the **GeoJSON file** generated from the previous assignment.
#
# Define the filename of the GeoJSON file containing previous results.

input_geojson_file = "/workspaces/geographic-coordinates-match-HultzHubbard/reverse-lookup/matched_nolli_features.geojson"

###############################
# 2) Load the GeoJSON data
###############################
# HINT: Use the `load_data()` function to read the JSON content of the file.
#       This will return a dictionary containing all matched & non-matched features.

geojson_data = load_data(input_geojson_file)

###############################
# 3) Split data between matched and non-matched entries
###############################
# HINT: The loaded data is structured as a **FeatureCollection**.
#       It contains both:
#       ✅ Matched Nolli entries (with an associated OSM feature)
#       ❌ Non-matched Nolli entries (without an OSM match)
#
# Your goal is to **separate** these two categories.

# Extract the list of features from the GeoJSON data
features = geojson_data.get("features", None)

# Initialize lists to store:
non_matched_data = []

for i in features:
    properties = i.get("properties", None)
    ifmatched = properties.get("Matched_Name", None)
    if ifmatched == None:
        add_props = {
            "Nolli_ID" : properties.get("Nolli_ID", None),
            "Nolli_Name" : properties.get("Nolli_Name", None),
        }
        non_matched_data.append({
            "type" : "Feature",
            "properties" : add_props,
            "geometry" : i.get("geometry", None)
        })

###############################
# 4) Filter out only the non-matched Nolli entries
###############################
# HINT: Now, filter `nolli_data` to **retain only** the Nolli features
#       that were **not previously matched**.
#

# Use the `matched_ids` list to check whether each Nolli feature is already matched.

# non_matched_data = []
# for each feature in nolli_data:
#    Extract the `Nolli_ID`
#    If `Nolli_ID` is NOT in `matched_ids`, append to `non_matched_data`

# NOTE: Use the `if not value in list:` syntax to check if an ID is in a list.

###############################
# 5) Load OSM features from the ZIP file
###############################
# HINT: Since we are performing a **reverse lookup**, we now need to:
# ✅ Extract OSM features from the `geojson_data.zip`
# ✅ Load the OSM dataset
#
# Use:
# - The proper functions to extract and load the OSM data from file

#zip_file = "/workspaces/geographic-coordinates-match-HultzHubbard/gottamatch-emall/geojson_data.zip"

# Extract

#geojson_files = ["nolli_points_open.geojson", "osm_node_way_relation.geojson"]

# extract_files(zip_file, geojson_files)

osm_file = load_data("/workspaces/geographic-coordinates-match-HultzHubbard/reverse-lookup/osm_node_way_relation.geojson")

modernFeatures = osm_file.get("features", None)
modernBuildings = []

for element in modernFeatures:
    modernBuildings.append({
        "type" : "Feature",
        "properties" : element.get("properties", None),
        "geometry" : element.get("geometry", None)
    })

###############################
# 6) Find the closest OSM match for each non-matched Nolli entry
###############################
# HINT: Instead of fuzzy matching, we now use **geographical proximity**.
#       We will:
#       - Extract **the centroid** of OSM features (using `shapely`).
#       - Measure the **distance** from each non-matched Nolli feature to the nearest OSM feature.
#       - Assign the closest OSM feature to each non-matched Nolli entry.
#
#       Luckily, you don't have to deal with it, because we created the function
#       `find_closest_matches`. Go to utils.py and find out how to use it!
#       Keep the use_geodesic flag to False, otherwise it will take too much time.
#

matches = find_closest_matches(non_matched_data, modernBuildings)

###############################
# 7) Save the new matches to JSON
###############################
# HINT: Now that we have found the closest matches for each of 
#       the previously non-matched entries, save the results as 
#       a Standard JSON format for analysis, and as a GeoJSON

# To convert it to GeoJSON format, use the convert_to_geojson(...) function

convert_to_geojson(matches, "geometry_matched_nolli_features.geojson")

###############################
# 8) Assignment Submission & Next Steps
###############################
# 🎯 **Final Task**: Verify the results!
# - Open your JSON file and check how well the new matches align.
# - Copy/paste your GeoJSON file in https://geojson.io/ and check it.
# - Submit a screenshot of a zoomed view of the GeoJSON together with your code
