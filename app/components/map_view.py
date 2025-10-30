import reflex as rx
import reflex_enterprise as rxe
from app.state import MapState
from app.states.upload_state import UploadState
from app.components.map_controls import map_controls, coordinate_display


def map_view() -> rx.Component:
    """The main map view component."""
    return rx.el.div(
        rxe.map(
            rxe.map.tile_layer(
                url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            ),
            rx.foreach(
                UploadState.data_points, lambda point: rxe.map.marker(position=point)
            ),
            map_controls(),
            coordinate_display(),
            id="main-map",
            center=MapState.center,
            zoom=MapState.zoom,
            height="100%",
            width="100%",
            zoom_control=False,
            on_click=MapState.handle_map_click,
            on_zoom=MapState.handle_zoom.debounce(100),
        ),
        class_name="relative flex-1 h-full w-full",
    )