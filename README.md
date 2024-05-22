# FastAPI Application

This FastAPI application provides endpoints for managing and analyzing geospatial data, including adding points to a PostgreSQL/PostGIS database, querying points within a polygon, and analyzing raster files.

## Features

- **Add Point:** Add a new point to the PostgreSQL/PostGIS database.
- **Points Within Polygon:** Retrieve points that fall within a specified polygon.
- **Analyze Raster:** Upload and analyze a raster file to extract statistical data.
- **Health Check:** Simple health check endpoint to ensure the service is running.

## Requirements

- Python 3.7+
- PostgreSQL with PostGIS extension
- The following Python packages:
  - fastapi
  - uvicorn
  - sqlalchemy
  - psycopg2-binary
  - geopandas
  - rasterio
  - pydantic
  - shapely
  - python-dotenv (for managing environment variables)

## Setup and Installation

- Clone the Repository

```bash
git clone https://github.com/kayung/fastapi-app.git
cd fastapi-app
 ``` 
- Set Up the Virtual Environment
- Create and activate a virtual environment:
```bash
 python -m venv venv
 ```
- Activate the environment
```bash
source venv/bin/activate  
# On Windows use `venv\Scripts\activate`
 ```


- Install Dependencies
- Install the required Python packages:
```bash
 pip install -r requirements.txt
 ```

- Configure PostgreSQL and PostGIS
- Ensure PostgreSQL and PostGIS are installed and configured:
```bash
 sudo apt-get install postgresql postgresql-contrib postgis
 ```

- Create the database and enable the PostGIS extension:
```bash
 sudo -u postgres psql
CREATE DATABASE mydatabase;
\c mydatabase;
CREATE EXTENSION postgis;
 ```
- Configure Environment Variables
- Create a .env file in the root directory and add your database URL:
```bash
 DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
 ```

## Run the Application
- Use uvicorn to run the FastAPI application:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
 ```










