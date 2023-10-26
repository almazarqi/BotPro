import geoip2.database

# Specify the relative path to the database file in the same folder as your script
database_file = '/Users/user/Library/CloudStorage/OneDrive-UniversityofGlasgow/Framwork/maps/GeoLite2-City_20231024/GeoLite2-City.mmdb'

# Create a Reader object
with geoip2.database.Reader(database_file) as reader:
    response = reader.city('200.77.22.90')
