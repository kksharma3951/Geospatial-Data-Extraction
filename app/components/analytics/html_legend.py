import reflex as rx
from app.states.analytics_state import AnalyticsState, ChartData


def legend_item(item: ChartData) -> rx.Component:
    """A single item in the custom HTML legend."""
    color_map = {
        "GeoJSON": "bg-blue-500",
        "KML": "bg-green-500",
        "CSV": "bg-yellow-500",
    }
    return rx.el.div(
        rx.el.div(
            class_name=f"w-3 h-3 rounded-full {color_map.get(item['name'], 'bg-gray-400')}"
        ),
        rx.el.span(item["name"], class_name="ml-2 text-sm text-gray-600"),
        rx.el.span(f"({item['value']})"),
        class_name="flex items-center",
    )


def html_legend() -> rx.Component:
    """Custom HTML legend for the pie chart."""
    return rx.el.div(
        rx.foreach(AnalyticsState.file_type_chart_data, legend_item),
        class_name="flex justify-center items-center gap-4 mt-4",
    )