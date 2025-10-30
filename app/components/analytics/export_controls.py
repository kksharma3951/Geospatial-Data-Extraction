import reflex as rx
from app.states.analytics_state import AnalyticsState


def export_controls() -> rx.Component:
    """Controls for exporting data."""
    return rx.el.div(
        rx.el.h3("Export Data", class_name="text-lg font-bold text-gray-800 mb-4"),
        rx.el.div(
            rx.el.button(
                rx.icon("file-down", class_name="h-4 w-4 mr-2"),
                "Export as CSV",
                on_click=AnalyticsState.export_csv,
                class_name="flex items-center w-full justify-center bg-green-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-green-700 transition-colors",
            ),
            rx.el.button(
                rx.icon("file-json-2", class_name="h-4 w-4 mr-2"),
                "Export as GeoJSON",
                on_click=AnalyticsState.export_geojson,
                class_name="flex items-center w-full justify-center bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
        ),
        class_name="p-6 bg-white border border-gray-200 rounded-lg shadow-sm",
    )