import reflex as rx
from app.components.sidebar import sidebar
from app.states.analytics_state import AnalyticsState
from app.components.analytics.stat_cards import stat_card_grid
from app.components.analytics.charts import file_type_distribution_chart
from app.components.analytics.export_controls import export_controls


def analytics_page() -> rx.Component:
    """The analytics dashboard page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Analytics Dashboard", class_name="text-2xl font-bold text-gray-900"
                ),
                class_name="h-16 flex items-center px-6 border-b border-gray-200 bg-white shadow-sm sticky top-0 z-10",
            ),
            rx.el.div(
                stat_card_grid(),
                rx.el.div(
                    file_type_distribution_chart(),
                    export_controls(),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start",
                ),
                class_name="flex-1 p-6 space-y-8",
            ),
            class_name="flex-1 flex flex-col h-screen overflow-y-auto",
        ),
        class_name="flex h-screen w-screen bg-gray-50 font-['Roboto']",
        on_mount=AnalyticsState.on_load,
    )