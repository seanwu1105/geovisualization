import sys

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from src.build_gui import build_gui
from src.build_renderer import build_renderer
from src.constants import ROTATION_X
from src.flat.get_texture import get_texture
from src.flat.parse_args import parse_args
from src.vtk_side_effects import import_for_rendering_core

DEFAULT_SCALE = 200


def build_vtk_widget(
    parent: QObject, elevation_mapper_filename: str, texture_filename: str
):
    def on_scale_changed(value: int):
        warp_scalar.SetScaleFactor(-value)
        widget.GetRenderWindow().Render()

    widget = QVTKRenderWindowInteractor(parent)

    elevation_mapper, warp_scalar = get_elevation_mapper_and_scalar(
        elevation_mapper_filename
    )
    texture = get_texture(texture_filename)

    actor = vtkActor()
    actor.SetMapper(elevation_mapper)
    actor.SetTexture(texture)
    actor.RotateX(ROTATION_X)

    renderer = build_renderer((actor,))

    widget.GetRenderWindow().AddRenderer(renderer)
    widget.GetRenderWindow().GetInteractor().Initialize()
    return widget, on_scale_changed


def get_elevation_mapper_and_scalar(filename: str):
    reader = vtkXMLImageDataReader()
    reader.SetFileName(filename)

    warp = vtkWarpScalar()
    warp.SetScaleFactor(-DEFAULT_SCALE)
    warp.SetInputConnection(reader.GetOutputPort())

    mapper = vtkDataSetMapper()
    mapper.SetScalarVisibility(False)
    mapper.SetInputConnection(warp.GetOutputPort())

    return mapper, warp


if __name__ == "__main__":
    import_for_rendering_core()
    args = parse_args()
    app = QApplication()
    gui = build_gui(args.geometry, args.image, build_vtk_widget, DEFAULT_SCALE)
    gui.show()
    sys.exit(app.exec())
