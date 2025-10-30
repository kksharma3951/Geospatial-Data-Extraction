import reflex as rx
from app.states.analytics_state import AnalyticsState
from app.components.analytics.html_legend import html_legend


def file_type_distribution_chart() -> rx.Component:
    """A pie chart showing the distribution of uploaded file types."""
    return rx.el.div(
        rx.el.h3(
            "File Type Distribution", class_name="text-lg font-bold text-gray-800 mb-4"
        ),
        rx.recharts.pie_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.pie(
                rx.foreach(
                    AnalyticsState.file_type_chart_data,
                    lambda item, index: rx.recharts.cell(
                        fill=rx.Var.create(["#3b82f6", "#10b981", "#f59e0b"])[index]
                    ),
                ),
                data=AnalyticsState.file_type_chart_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                outer_radius=80,
                label=True,
                stroke="#fff",
                stroke_width=2,
            ),
            width="100%",
            height=300,
        ),
        html_legend(),
        class_name="p-6 bg-white border border-gray-200 rounded-lg shadow-sm",
    )