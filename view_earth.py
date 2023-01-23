import argparse
import sys

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from src.build_gui import build_gui
from src.build_renderer import build_renderer
from src.constants import ROTATION_X
from src.flat.get_texture import get_texture
from src.get_tubed_actor import get_tubed_actor
from src.vtk_side_effects import import_for_rendering_core

DEFAULT_SCALE = 50


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--geometry", default="assets/elevation_sphere_small.vtp")
    parser.add_argument(
        "-i", "--image", default="assets/world.topo.bathy.200408.medium.jpg"
    )

    return parser.parse_args()


# pylint: disable=too-many-locals
def build_vtk_widget(parent: QObject, elevation_filename: str, texture_filename: str):
    def on_scale_changed(value: int):
        elevation_warp.SetScaleFactor(value)
        contour_warp.SetScaleFactor(value)
        sea_level_warp.SetScaleFactor(value)
        widget.GetRenderWindow().Render()

    widget = QVTKRenderWindowInteractor(parent)

    elevation_reader = vtkXMLPolyDataReader()
    elevation_reader.SetFileName(elevation_filename)

    elevation_warp = vtkWarpScalar()
    elevation_warp.SetScaleFactor(DEFAULT_SCALE)
    elevation_warp.SetInputConnection(elevation_reader.GetOutputPort())

    elevation_mapper = vtkDataSetMapper()
    elevation_mapper.SetScalarVisibility(False)
    elevation_mapper.SetInputConnection(elevation_warp.GetOutputPort())

    texture = get_texture(texture_filename)

    elevation_actor = vtkActor()
    elevation_actor.RotateX(ROTATION_X)
    elevation_actor.SetMapper(elevation_mapper)
    elevation_actor.SetTexture(texture)

    contour_filter = vtkContourFilter()
    contour_filter.GenerateValues(19, -10_000, 8_000)
    contour_filter.SetInputConnection(elevation_reader.GetOutputPort())

    contour_warp = vtkWarpScalar()
    contour_warp.SetScaleFactor(DEFAULT_SCALE)
    contour_warp.SetInputConnection(contour_filter.GetOutputPort())

    contour_tube_actor = get_tubed_actor(
        contour_warp.GetOutputPort(), 10000, "LightGreen"
    )

    sea_level_filter = vtkContourFilter()
    sea_level_filter.SetValue(0, 0)
    sea_level_filter.SetInputConnection(elevation_reader.GetOutputPort())

    sea_level_warp = vtkWarpScalar()
    sea_level_warp.SetScaleFactor(DEFAULT_SCALE)
    sea_level_warp.SetInputConnection(sea_level_filter.GetOutputPort())

    sea_level_tube_actor = get_tubed_actor(sea_level_warp.GetOutputPort(), 15000, "Red")

    renderer = build_renderer(
        (elevation_actor, contour_tube_actor, sea_level_tube_actor)
    )

    widget.GetRenderWindow().AddRenderer(renderer)
    widget.GetRenderWindow().GetInteractor().Initialize()
    return widget, on_scale_changed


if __name__ == "__main__":
    import_for_rendering_core()
    args = parse_args()
    app = QApplication()
    gui = build_gui(args.geometry, args.image, build_vtk_widget, DEFAULT_SCALE)
    gui.show()
    sys.exit(app.exec())
