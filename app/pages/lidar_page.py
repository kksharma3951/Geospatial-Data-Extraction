import reflex as rx
from app.components.sidebar import sidebar
from app.states.lidar_state import LidarState


def lidar_upload_component() -> rx.Component:
    """Component for uploading LiDAR files."""
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud-upload", class_name="w-12 h-12 text-gray-400"),
                rx.el.p(
                    "Drag & drop a LAS/LAZ file, or click to select",
                    class_name="text-sm text-gray-500 mt-2",
                ),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer",
            ),
            id="lidar-upload",
            accept={"application/octet-stream": [".las", ".laz"]},
            multiple=False,
            on_drop=LidarState.handle_lidar_upload(
                rx.upload_files(upload_id="lidar-upload")
            ),
            class_name="w-full",
        ),
        rx.el.button(
            "Process Selected File",
            on_click=LidarState.handle_lidar_upload(
                rx.upload_files(upload_id="lidar-upload")
            ),
            is_loading=LidarState.is_uploading,
            class_name="mt-4 w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors",
        ),
        rx.cond(
            LidarState.is_uploading,
            rx.el.div("Processing...", rx.el.progress(is_indeterminate=True)),
        ),
        class_name="w-full max-w-lg mx-auto",
    )


def metadata_display() -> rx.Component:
    """Displays metadata of the uploaded LiDAR file."""
    return rx.cond(
        LidarState.metadata,
        rx.el.div(
            rx.el.h3(
                "LiDAR Metadata", class_name="text-lg font-bold text-gray-800 mb-4"
            ),
            rx.el.div(
                rx.el.p(rx.el.strong("File:"), f" {LidarState.metadata['file_name']}"),
                rx.el.p(
                    rx.el.strong("Points:"), f" {LidarState.metadata['point_count']}"
                ),
                rx.el.p(
                    rx.el.strong("Format:"), f" {LidarState.metadata['point_format']}"
                ),
                rx.el.p(
                    rx.el.strong("Bounds Min:"),
                    f" {LidarState.metadata['min_bounds'].to_string()}",
                ),
                rx.el.p(
                    rx.el.strong("Bounds Max:"),
                    f" {LidarState.metadata['max_bounds'].to_string()}",
                ),
                rx.el.p(
                    rx.el.strong("Classes:"),
                    f" {LidarState.metadata['classifications'].to_string()}",
                ),
                class_name="text-sm space-y-1",
            ),
            class_name="p-6 bg-white border border-gray-200 rounded-lg shadow-sm mt-8",
        ),
        None,
    )


def point_cloud_viewer() -> rx.Component:
    """Displays the 3D point cloud visualization."""
    return rx.cond(
        LidarState.point_cloud_fig,
        rx.el.div(
            rx.el.h3(
                "3D Point Cloud Viewer",
                class_name="text-lg font-bold text-gray-800 mb-4",
            ),
            rx.plotly(data=LidarState.point_cloud_fig, height="600px"),
            class_name="p-6 bg-white border border-gray-200 rounded-lg shadow-sm mt-8",
        ),
        rx.el.div(
            rx.el.p(
                "Upload a LiDAR file to see the 3D visualization.",
                class_name="text-center text-gray-500 py-20",
            ),
            class_name="p-6 bg-white border border-gray-200 rounded-lg shadow-sm mt-8",
        ),
    )


def lidar_page() -> rx.Component:
    """The LiDAR data processing and visualization page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "LiDAR Processing", class_name="text-2xl font-bold text-gray-900"
                ),
                class_name="h-16 flex items-center px-6 border-b border-gray-200 bg-white shadow-sm sticky top-0 z-10",
            ),
            rx.el.div(
                lidar_upload_component(),
                metadata_display(),
                point_cloud_viewer(),
                class_name="flex-1 p-6 space-y-8",
            ),
            class_name="flex-1 flex flex-col h-screen overflow-y-auto",
        ),
        class_name="flex h-screen w-screen bg-gray-50 font-['Roboto']",
    )