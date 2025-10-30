import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import LatLng, latlng
from typing import TypedDict, Any


class NavItem(TypedDict):
    name: str
    icon: str
    href: str


class MapState(rx.State):
    """The state for the map application."""

    center: LatLng = latlng(lat=34.0522, lng=-118.2437)
    zoom: float = 10.0
    clicked_coordinates: LatLng | None = None
    sidebar_open: bool = True
    nav_items: list[NavItem] = [
        {"name": "Map", "icon": "map", "href": "/"},
        {"name": "Data Upload", "icon": "upload", "href": "/upload"},
        {"name": "Analytics", "icon": "bar-chart-2", "href": "/analytics"},
        {"name": "LiDAR", "icon": "cube", "href": "/lidar"},
        {"name": "Settings", "icon": "settings", "href": "#"},
    ]

    @rx.event
    def toggle_sidebar(self):
        """Toggles the sidebar open/closed."""
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def handle_map_click(self, event_args: dict[str, Any]):
        """Handles map click events and updates coordinates."""
        lat = round(event_args["latlng"]["lat"], 6)
        lng = round(event_args["latlng"]["lng"], 6)
        self.clicked_coordinates = latlng(lat=lat, lng=lng)

    @rx.event
    def handle_zoom(self, event_args: dict[str, Any]):
        """Handles map zoom events."""
        self.zoom = event_args["target"]["zoom"]

    @rx.event
    def reset_view(self):
        """Resets the map to the initial center and zoom."""
        self.center = latlng(lat=34.0522, lng=-118.2437)
        self.zoom = 10.0
        self.clicked_coordinates = None