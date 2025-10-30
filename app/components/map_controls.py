import reflex as rx
import reflex_enterprise as rxe
from app.state import MapState


def map_controls() -> rx.Component:
    """Controls for the map, including zoom and coordinate display."""
    map_api = rxe.map.api("main-map")
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("zoom-in", class_name="h-4 w-4"),
                on_click=map_api.zoom_in(1),
                class_name="p-2 bg-white rounded-t-lg border-b border-gray-200 cursor-pointer hover:bg-gray-50 shadow-md",
            ),
            rx.el.div(
                rx.icon("zoom-out", class_name="h-4 w-4"),
                on_click=map_api.zoom_out(1),
                class_name="p-2 bg-white rounded-b-lg cursor-pointer hover:bg-gray-50 shadow-md",
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.icon("locate-fixed", class_name="h-4 w-4"),
            on_click=MapState.reset_view,
            class_name="p-2 bg-white rounded-lg cursor-pointer hover:bg-gray-50 shadow-md",
        ),
        class_name="absolute top-4 right-4 z-[1000] flex flex-col gap-2",
    )


def coordinate_display() -> rx.Component:
    """Displays the current map coordinates."""
    return rx.el.div(
        rx.el.div(
            rx.el.span("Lat:", class_name="font-semibold text-gray-600"),
            rx.el.span(
                rx.cond(
                    MapState.clicked_coordinates,
                    MapState.clicked_coordinates["lat"].to_string(),
                    "N/A",
                ),
                class_name="ml-1 text-gray-800",
            ),
        ),
        rx.el.div(
            rx.el.span("Lng:", class_name="font-semibold text-gray-600"),
            rx.el.span(
                rx.cond(
                    MapState.clicked_coordinates,
                    MapState.clicked_coordinates["lng"].to_string(),
                    "N/A",
                ),
                class_name="ml-1 text-gray-800",
            ),
        ),
        rx.el.div(
            rx.el.span("Zoom:", class_name="font-semibold text-gray-600"),
            rx.el.span(MapState.zoom.to_string(), class_name="ml-1 text-gray-800"),
        ),
        class_name="absolute bottom-4 left-4 z-[1000] bg-white bg-opacity-80 backdrop-blur-sm p-2 rounded-lg shadow-md text-xs flex gap-4 border border-gray-200",
    )