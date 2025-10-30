import reflex as rx
import plotly.graph_objects as go
import numpy as np
import laspy
import logging
from typing import Any, TypedDict


class LidarMetadata(TypedDict):
    file_name: str
    point_count: int
    point_format: str
    min_bounds: list[float]
    max_bounds: list[float]
    classifications: list[int]


class LidarState(rx.State):
    """State for handling LiDAR data processing and visualization."""

    uploaded_file: str = ""
    is_uploading: bool = False
    metadata: LidarMetadata | None = None
    point_cloud_fig: go.Figure | None = None
    downsample_factor: int = 100

    @rx.event
    async def handle_lidar_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of a single LAS/LAZ file."""
        if not files:
            yield rx.toast.error("No file selected.")
            return
        self.is_uploading = True
        yield
        try:
            file = files[0]
            upload_data = await file.read()
            self.uploaded_file = file.name
            with laspy.open(upload_data) as las_file:
                self.metadata = {
                    "file_name": file.name,
                    "point_count": las_file.header.point_count,
                    "point_format": str(las_file.header.point_format.id),
                    "min_bounds": [round(val, 2) for val in las_file.header.min],
                    "max_bounds": [round(val, 2) for val in las_file.header.max],
                    "classifications": np.unique(
                        np.array(las_file.classification)
                    ).tolist(),
                }
                points = las_file.read_points(las_file.header.point_count)
                step = max(1, self.downsample_factor)
                x = points.x[::step]
                y = points.y[::step]
                z = points.z[::step]
            self.point_cloud_fig = self._create_3d_scatter(x, y, z)
            yield rx.toast.success(f"Processed {file.name}")
        except Exception as e:
            logging.exception(f"Failed to process LiDAR file: {e}")
            yield rx.toast.error(f"Processing failed: An error occurred.")
        finally:
            self.is_uploading = False

    def _create_3d_scatter(
        self, x: np.ndarray, y: np.ndarray, z: np.ndarray
    ) -> go.Figure:
        """Create a 3D scatter plot for the point cloud."""
        fig = go.Figure(
            data=[
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    mode="markers",
                    marker={
                        "size": 1,
                        "color": z,
                        "colorscale": "Viridis",
                        "opacity": 0.7,
                    },
                )
            ]
        )
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
        )
        return fig