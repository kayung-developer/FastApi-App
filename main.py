from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import geopandas as gpd
from shapely.geometry import Point
import rasterio
import os
from typing import List
import uvicorn

# Define the FastAPI app
app = FastAPI()

# Define the SQLAlchemy database URL
DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Pydantic model for request validation
class Coordinates(BaseModel):
    latitude: float
    longitude: float


class PolygonRequest(BaseModel):
    coordinates: List[Coordinates]


# Endpoint to add a new point to the database
@app.post("/add_point")
def add_point(coord: Coordinates):
    db = SessionLocal()
    try:
        point = Point(coord.longitude, coord.latitude)
        # Save the point to the database using GeoPandas
        gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[point])
        gdf.to_postgis(name='points', con=db.connection(), if_exists='append')
        return {"message": "Point added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# Endpoint to retrieve points within a polygon
@app.post("/points_within_polygon")
def points_within_polygon(polygon: PolygonRequest):
    db = SessionLocal()
    try:
        polygon_coords = [(coord.longitude, coord.latitude) for coord in polygon.coordinates]
        polygon_geom = Polygon(polygon_coords)
        sql = f"SELECT * FROM points WHERE ST_Contains(ST_GeomFromText('{polygon_geom.wkt}', 4326), geom)"
        points_within = gpd.read_postgis(sql, db.connection())
        return JSONResponse(content=points_within.to_json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# Function to analyze a raster file
def analyze_raster(file_path: str):
    with rasterio.open(file_path) as src:
        array = src.read(1)
        stats = {
            "min": array.min(),
            "max": array.max(),
            "mean": array.mean(),
            "std": array.std()
        }
    return stats


# Endpoint to upload and analyze a raster file
@app.post("/analyze_raster")
def upload_and_analyze_raster(file: bytes):
    file_path = "/tmp/temp_raster.tif"
    with open(file_path, "wb") as f:
        f.write(file)

    stats = analyze_raster(file_path)
    os.remove(file_path)
    return stats


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



#Developed by Pascal Saviour