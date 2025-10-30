import reflex as rx
from app.state import MapState, NavItem


def nav_item(item: NavItem) -> rx.Component:
    """A single navigation item in the sidebar."""
    return rx.el.a(
        rx.icon(
            item["icon"],
            class_name="h-5 w-5 text-gray-500 group-hover:text-blue-600 transition-colors",
        ),
        rx.cond(
            MapState.sidebar_open,
            rx.el.span(
                item["name"],
                class_name="ml-3 text-sm font-medium text-gray-700 group-hover:text-blue-600 transition-colors",
            ),
            None,
        ),
        href=item["href"],
        class_name="flex items-center p-2 rounded-lg hover:bg-blue-50 group transition-all",
    )


def sidebar() -> rx.Component:
    """The main sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("globe", class_name="h-8 w-8 text-blue-600"),
                rx.cond(
                    MapState.sidebar_open,
                    rx.el.h1(
                        "GeoExtract", class_name="text-xl font-bold text-gray-800 ml-2"
                    ),
                    None,
                ),
                class_name="flex items-center p-4 border-b border-gray-200 h-16",
            ),
            rx.el.nav(
                rx.foreach(MapState.nav_items, nav_item),
                class_name="flex-1 px-2 py-4 space-y-1",
            ),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(
                    rx.cond(MapState.sidebar_open, "chevrons-left", "chevrons-right"),
                    class_name="h-5 w-5 text-gray-600",
                ),
                on_click=MapState.toggle_sidebar,
                class_name="p-2 rounded-lg hover:bg-gray-100 transition-colors",
            ),
            class_name="p-2 border-t border-gray-200",
        ),
        class_name=rx.cond(
            MapState.sidebar_open,
            "w-64 bg-white border-r border-gray-200 flex flex-col transition-all duration-300 ease-in-out",
            "w-16 bg-white border-r border-gray-200 flex flex-col transition-all duration-300 ease-in-out",
        ),
    )