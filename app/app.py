import reflex as rx
import reflex_enterprise as rxe
from app.components.sidebar import sidebar
from app.components.map_view import map_view
from app.pages.upload_page import upload_page
from app.pages.analytics_page import analytics_page
from app.pages.lidar_page import lidar_page


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Geospatial Data Extraction",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                class_name="h-16 flex items-center px-6 border-b border-gray-200 bg-white shadow-sm",
            ),
            rx.el.div(map_view(), class_name="flex-1 p-4"),
            class_name="flex-1 flex flex-col h-screen",
        ),
        class_name="flex h-screen w-screen bg-gray-50 font-['Roboto']",
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=",
            cross_origin="",
        ),
    ],
)
app.add_page(index)
app.add_page(upload_page, route="/upload")
app.add_page(analytics_page, route="/analytics")
app.add_page(lidar_page, route="/lidar")