from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from src.build_renderer import build_renderer
from src.constants import ROTATION_X
from src.flat.get_texture import get_texture
from src.flat.parse_args import parse_args
from src.get_tubed_actor import get_tubed_actor
from src.vtk_side_effects import import_for_rendering_core


def render(elevation_mapper_filename: str, texture_filename: str):
    elevation_reader = vtkXMLImageDataReader()
    elevation_reader.SetFileName(elevation_mapper_filename)

    elevation_mapper = vtkDataSetMapper()
    elevation_mapper.SetScalarVisibility(False)
    elevation_mapper.SetInputConnection(elevation_reader.GetOutputPort())

    texture = get_texture(texture_filename)

    elevation_actor = vtkActor()
    elevation_actor.SetMapper(elevation_mapper)
    elevation_actor.SetTexture(texture)
    elevation_actor.RotateX(ROTATION_X)

    contour_filter = vtkContourFilter()
    contour_filter.GenerateValues(19, -10_000, 8_000)
    contour_filter.SetInputConnection(elevation_reader.GetOutputPort())

    contour_tube_actor = get_tubed_actor(
        contour_filter.GetOutputPort(), 10000, "LightGreen"
    )

    sea_level_filter = vtkContourFilter()
    sea_level_filter.SetValue(0, 0)
    sea_level_filter.SetInputConnection(elevation_reader.GetOutputPort())

    sea_level_tube_actor = get_tubed_actor(
        sea_level_filter.GetOutputPort(), 11000, "Red"
    )

    renderer = build_renderer(
        (elevation_actor, contour_tube_actor, sea_level_tube_actor)
    )

    window = vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(640, 480)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.Initialize()

    return interactor


if __name__ == "__main__":
    import_for_rendering_core()

    args = parse_args()

    render(args.geometry, args.image).Start()
