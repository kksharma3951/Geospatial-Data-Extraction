import reflex as rx
from app.states.analytics_state import AnalyticsState, StatCard


def stat_card(stat: StatCard) -> rx.Component:
    """A card displaying a single statistic."""
    return rx.el.div(
        rx.el.div(
            rx.icon(stat["icon"], class_name="w-6 h-6 text-gray-500"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(stat["name"], class_name="text-sm font-medium text-gray-600"),
            rx.el.p(stat["value"], class_name="text-2xl font-bold text-gray-900"),
            class_name="ml-4",
        ),
        class_name="flex items-center p-4 bg-white border border-gray-200 rounded-lg shadow-sm",
    )


def stat_card_grid() -> rx.Component:
    """A grid of statistic cards."""
    return rx.el.div(
        rx.foreach(AnalyticsState.stats, stat_card),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",
    )