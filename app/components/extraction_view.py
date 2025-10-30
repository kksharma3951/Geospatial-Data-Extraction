import reflex as rx
from app.states.upload_state import UploadState


def extraction_controls() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Data Extraction & Filters",
            class_name="text-lg font-bold text-gray-800 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        on_change=UploadState.set_bbox_enabled,
                        checked=UploadState.bbox_enabled,
                        class_name="mr-2",
                    ),
                    "Bounding Box Filter",
                    class_name="flex items-center font-semibold text-gray-700",
                ),
                rx.cond(
                    UploadState.bbox_enabled,
                    rx.el.div(
                        rx.el.div(
                            rx.el.input(
                                placeholder="Min Lat",
                                on_change=lambda v: UploadState.set_bbox_value(
                                    "min_lat", v
                                ),
                                class_name="w-full p-2 border rounded-md text-sm",
                            ),
                            rx.el.input(
                                placeholder="Min Lng",
                                on_change=lambda v: UploadState.set_bbox_value(
                                    "min_lng", v
                                ),
                                class_name="w-full p-2 border rounded-md text-sm",
                            ),
                            rx.el.input(
                                placeholder="Max Lat",
                                on_change=lambda v: UploadState.set_bbox_value(
                                    "max_lat", v
                                ),
                                class_name="w-full p-2 border rounded-md text-sm",
                            ),
                            rx.el.input(
                                placeholder="Max Lng",
                                on_change=lambda v: UploadState.set_bbox_value(
                                    "max_lng", v
                                ),
                                class_name="w-full p-2 border rounded-md text-sm",
                            ),
                            class_name="grid grid-cols-2 gap-2 mt-2",
                        ),
                        class_name="p-4 bg-gray-50 rounded-lg mt-2 border",
                    ),
                    None,
                ),
                class_name="p-4 border rounded-lg bg-white shadow-sm",
            ),
            rx.el.button(
                "Apply Filters",
                on_click=UploadState.apply_filters,
                class_name="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors mt-4",
            ),
            class_name="space-y-4",
        ),
        class_name="w-full max-w-2xl mx-auto mt-8",
    )


def coordinate_converter() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Coordinate Converter", class_name="text-lg font-bold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.el.input(
                placeholder="e.g., 34.0522, -118.2437",
                on_change=UploadState.set_coord_input,
                class_name="w-full p-2 border rounded-md",
            ),
            rx.el.select(
                rx.el.option("WGS84 (Default)", value="wgs84"),
                rx.el.option("UTM", value="utm"),
                rx.el.option("Web Mercator", value="web_mercator"),
                on_change=UploadState.set_coord_system,
                value=UploadState.coord_system,
                class_name="w-full p-2 border rounded-md bg-white",
            ),
            rx.el.button(
                "Convert",
                on_click=UploadState.convert_coordinates,
                class_name="w-full bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-gray-700 transition-colors",
            ),
            rx.el.div(
                rx.el.p("Converted:", class_name="font-semibold"),
                rx.el.p(
                    UploadState.converted_coords,
                    class_name="text-sm font-mono bg-gray-100 p-2 rounded",
                ),
                class_name="mt-2",
            ),
            class_name="space-y-3 p-4 border rounded-lg bg-white shadow-sm",
        ),
        class_name="w-full max-w-2xl mx-auto mt-8",
    )


def extracted_data_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Extracted Data", class_name="text-lg font-bold text-gray-800 mb-4"),
        rx.cond(
            UploadState.extracted_points.length() > 0,
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Latitude", class_name="px-4 py-2 text-left"),
                            rx.el.th("Longitude", class_name="px-4 py-2 text-left"),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            UploadState.extracted_points,
                            lambda point: rx.el.tr(
                                rx.el.td(
                                    point["lat"].to_string(),
                                    class_name="px-4 py-2 border-t",
                                ),
                                rx.el.td(
                                    point["lng"].to_string(),
                                    class_name="px-4 py-2 border-t",
                                ),
                                class_name="hover:bg-gray-50",
                            ),
                        )
                    ),
                    class_name="w-full text-sm table-auto",
                ),
                class_name="overflow-x-auto border rounded-lg bg-white",
            ),
            rx.el.p(
                "No data extracted. Upload a file and apply filters.",
                class_name="text-sm text-gray-500",
            ),
        ),
        class_name="w-full max-w-2xl mx-auto mt-8",
    )