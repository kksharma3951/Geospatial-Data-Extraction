import reflex as rx
from app.states.upload_state import UploadState


def upload_component() -> rx.Component:
    """The file upload component."""
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud_upload", class_name="w-12 h-12 text-gray-400"),
                rx.el.p(
                    "Drag & drop files here, or click to select files",
                    class_name="text-sm text-gray-500 mt-2",
                ),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer",
            ),
            id="upload-area",
            accept={
                "application/json": [".geojson"],
                "application/vnd.google-earth.kml+xml": [".kml"],
                "text/csv": [".csv"],
            },
            multiple=True,
            max_files=10,
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.h3("Selected Files:", class_name="font-semibold text-gray-700"),
            rx.cond(
                rx.selected_files("upload-area").length() > 0,
                rx.foreach(
                    rx.selected_files("upload-area"),
                    lambda file: rx.el.div(
                        rx.icon("file", class_name="h-4 w-4 mr-2 text-gray-500"),
                        rx.el.span(file, class_name="text-sm text-gray-800"),
                        class_name="flex items-center p-2 bg-gray-100 rounded-md",
                    ),
                ),
                rx.el.p("No files selected.", class_name="text-sm text-gray-500"),
            ),
            class_name="mt-4 space-y-2",
        ),
        rx.el.button(
            "Upload",
            on_click=UploadState.handle_upload(
                rx.upload_files(upload_id="upload-area")
            ),
            class_name="mt-4 w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-300",
            disabled=UploadState.uploading,
        ),
        rx.cond(
            UploadState.uploading,
            rx.el.div(
                rx.el.progress(
                    value=UploadState.upload_progress, max=100, class_name="w-full mt-2"
                ),
                rx.el.p(
                    f"Uploading... {UploadState.upload_progress}%",
                    class_name="text-sm text-gray-600 text-center mt-1",
                ),
            ),
        ),
        class_name="w-full max-w-2xl mx-auto",
    )


def uploaded_files_list() -> rx.Component:
    """A list of already uploaded files."""
    return rx.el.div(
        rx.el.h3("Uploaded Files", class_name="text-lg font-bold text-gray-800 mb-4"),
        rx.cond(
            UploadState.uploaded_files.length() > 0,
            rx.el.ul(
                rx.foreach(
                    UploadState.uploaded_files,
                    lambda filename: rx.el.li(
                        rx.icon(
                            "square_check", class_name="h-5 w-5 text-green-500 mr-3"
                        ),
                        rx.el.span(filename, class_name="font-medium text-gray-700"),
                        class_name="flex items-center p-3 bg-white rounded-lg border border-gray-200 shadow-sm",
                    ),
                ),
                class_name="space-y-3",
            ),
            rx.el.p(
                "No files have been uploaded yet.", class_name="text-sm text-gray-500"
            ),
        ),
        class_name="w-full max-w-2xl mx-auto mt-8 p-6 bg-gray-50 rounded-lg border border-gray-200",
    )