import reflex as rx
import json
import logging
from reflex_enterprise.components.map.types import LatLng, latlng
from typing import Any, TypedDict
import csv
import xml.etree.ElementTree as ET


class Bbox(TypedDict):
    min_lat: float
    min_lng: float
    max_lat: float
    max_lng: float


class UploadState(rx.State):
    """State for handling file uploads and processing geospatial data."""

    uploaded_files: list[str] = []
    uploading: bool = False
    upload_progress: int = 0
    data_points: list[LatLng] = []
    extracted_points: list[LatLng] = []
    bbox_enabled: bool = False
    radius_enabled: bool = False
    bbox: Bbox = {"min_lat": 0, "min_lng": 0, "max_lat": 0, "max_lng": 0}
    radius_center: LatLng | None = None
    radius_km: float = 1.0
    coord_input: str = ""
    coord_system: str = "wgs84"
    converted_coords: str = ""

    async def _parse_geojson(self, content: str):
        data = json.loads(content)
        for feature in data.get("features", []):
            if feature["geometry"]["type"] == "Point":
                coords = feature["geometry"]["coordinates"]
                self.data_points.append(latlng(lat=coords[1], lng=coords[0]))

    async def _parse_kml(self, content: str):
        root = ET.fromstring(content)
        for placemark in root.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
            point = placemark.find(".//{http://www.opengis.net/kml/2.2}Point")
            if point is not None:
                coords_text = point.find(
                    ".//{http://www.opengis.net/kml/2.2}coordinates"
                )
                if coords_text is not None and coords_text.text:
                    coords = coords_text.text.strip().split(",")
                    if len(coords) >= 2:
                        self.data_points.append(
                            latlng(lat=float(coords[1]), lng=float(coords[0]))
                        )

    async def _parse_csv(self, content: str):
        reader = csv.DictReader(content.splitlines())
        for row in reader:
            lat = row.get("lat") or row.get("latitude")
            lon = row.get("lon") or row.get("lng") or row.get("longitude")
            if lat and lon:
                self.data_points.append(latlng(lat=float(lat), lng=float(lon)))

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle file upload, parse data, and update progress."""
        if not files:
            yield rx.toast.error("No files selected.")
            return
        self.uploading = True
        self.data_points = []
        self.extracted_points = []
        yield
        for i, file in enumerate(files):
            upload_data = await file.read()
            output_path = rx.get_upload_dir() / file.name
            with output_path.open("wb") as f:
                f.write(upload_data)
            self.uploaded_files.append(file.name)
            try:
                content = upload_data.decode("utf-8")
                if file.name.endswith(".geojson"):
                    await self._parse_geojson(content)
                elif file.name.endswith(".kml"):
                    await self._parse_kml(content)
                elif file.name.endswith(".csv"):
                    await self._parse_csv(content)
            except Exception as e:
                logging.exception(f"Error parsing {file.name}: {e}")
                yield rx.toast.error(f"Failed to parse {file.name}: {str(e)}")
            self.upload_progress = int((i + 1) / len(files) * 100)
            yield
        self.uploading = False
        self.extracted_points = self.data_points
        yield rx.toast.success(
            f"Processed {len(self.data_points)} points from {len(files)} file(s)."
        )

    @rx.event
    def set_bbox_value(self, key: str, value: str):
        """Update a value in the bounding box dictionary."""
        try:
            self.bbox[key] = float(value)
        except (ValueError, TypeError) as e:
            logging.exception(f"Error setting bbox value: {e}")

    @rx.event
    def apply_filters(self):
        """Apply currently enabled filters to the data points."""
        filtered = self.data_points
        if self.bbox_enabled:
            b = self.bbox
            filtered = [
                p
                for p in filtered
                if b["min_lat"] <= p["lat"] <= b["max_lat"]
                and b["min_lng"] <= p["lng"] <= b["max_lng"]
            ]
        self.extracted_points = filtered
        yield rx.toast.info(
            f"Found {len(self.extracted_points)} points after filtering."
        )

    @rx.event
    async def convert_coordinates(self):
        """Convert coordinates from input string."""
        try:
            lat, lon = map(float, self.coord_input.split(","))
            if self.coord_system == "utm":
                easting = (lon + 180) * 10000
                northing = lat * 10000
                self.converted_coords = (
                    f"Zone 11N, Easting: {easting:.2f}, Northing: {northing:.2f}"
                )
            elif self.coord_system == "web_mercator":
                self.converted_coords = (
                    f"X: {lon * 20037508.34 / 180}, Y: {lat * 20037508.34 / 180}"
                )
            else:
                self.converted_coords = "Select a target system."
        except Exception as e:
            logging.exception(f"Error converting coordinates: {e}")
            self.converted_coords = f"Error: {e}"