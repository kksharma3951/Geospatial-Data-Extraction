import reflex as rx
from typing import TypedDict, Any
from app.states.upload_state import UploadState
import json
import csv
from io import StringIO


class StatCard(TypedDict):
    name: str
    value: str
    icon: str


class ChartData(TypedDict):
    name: str
    value: int


class AnalyticsState(rx.State):
    """State for the analytics dashboard."""

    stats: list[StatCard] = []
    file_type_chart_data: list[ChartData] = []

    async def _update_stats(self):
        upload_state = await self.get_state(UploadState)
        self.stats = [
            {
                "name": "Total Data Points",
                "value": str(len(upload_state.data_points)),
                "icon": "map-pin",
            },
            {
                "name": "Uploaded Files",
                "value": str(len(upload_state.uploaded_files)),
                "icon": "file",
            },
            {
                "name": "Bounding Box Active",
                "value": "Yes" if upload_state.bbox_enabled else "No",
                "icon": "scan",
            },
            {
                "name": "Extracted Points",
                "value": str(len(upload_state.extracted_points)),
                "icon": "filter",
            },
        ]
        self.file_type_chart_data = [
            {
                "name": "GeoJSON",
                "value": sum(
                    (1 for f in upload_state.uploaded_files if f.endswith(".geojson"))
                ),
            },
            {
                "name": "KML",
                "value": sum(
                    (1 for f in upload_state.uploaded_files if f.endswith(".kml"))
                ),
            },
            {
                "name": "CSV",
                "value": sum(
                    (1 for f in upload_state.uploaded_files if f.endswith(".csv"))
                ),
            },
        ]

    @rx.event
    async def on_load(self):
        """Load the analytics data."""
        await self._update_stats()

    @rx.event
    def export_csv(self) -> rx.event.EventSpec:
        """Export extracted data to CSV."""
        upload_state = yield UploadState.get_state()
        string_io = StringIO()
        writer = csv.writer(string_io)
        writer.writerow(["latitude", "longitude"])
        for point in upload_state.extracted_points:
            writer.writerow([point["lat"], point["lng"]])
        csv_bytes = string_io.getvalue().encode()
        return rx.download(
            data=csv_bytes, filename="extracted_data.csv", content_type="text/csv"
        )

    @rx.event
    def export_geojson(self) -> rx.event.EventSpec:
        """Export extracted data to GeoJSON."""
        upload_state = yield UploadState.get_state()
        features = []
        for point in upload_state.extracted_points:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [point["lng"], point["lat"]],
                },
                "properties": {},
            }
            features.append(feature)
        geojson_data = {"type": "FeatureCollection", "features": features}
        geojson_str = json.dumps(geojson_data, indent=2).encode()
        return rx.download(
            data=geojson_str,
            filename="extracted_data.geojson",
            content_type="application/json",
        )