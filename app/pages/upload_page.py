import reflex as rx
from app.components.sidebar import sidebar
from app.components.upload_view import upload_component, uploaded_files_list
from app.components.extraction_view import (
    extraction_controls,
    coordinate_converter,
    extracted_data_table,
)


def upload_page() -> rx.Component:
    """The data upload page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1("Data Upload", class_name="text-2xl font-bold text-gray-900"),
                class_name="h-16 flex items-center px-6 border-b border-gray-200 bg-white shadow-sm sticky top-0 z-10",
            ),
            rx.el.div(
                upload_component(),
                uploaded_files_list(),
                extraction_controls(),
                coordinate_converter(),
                extracted_data_table(),
                class_name="flex-1 p-6 space-y-8",
            ),
            class_name="flex-1 flex flex-col h-screen overflow-y-auto",
        ),
        class_name="flex h-screen w-screen bg-gray-50 font-['Roboto']",
    )