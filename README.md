# gis-server
A Geospatial Rest Backend Using GeoDjango

# stack
* Python

* Django/Geodjango

* PostgreSQL/PostGIS

* Django Rest Framework

# What can it do
* CRUD models (country, city, capital)

* Bbox - filters to find all objects inside the area, given by 4 coordinates

* Calculates the sum of the areas of all objects, that satisfy the filter conditions

* Returns data for all cities located in inside some country

# How to use
## Installation:

1. Install `requirements.txt`
2. `cd geoserver`
3. Create `.env` file:

    ```
    GDAL_DLL_PATH=<your_gdal_path>
    DB_NAME=<your_db_name>
    DB_USER_NAME=<your_user_name>
    DB_PASSWORD=<your_password>
    ```