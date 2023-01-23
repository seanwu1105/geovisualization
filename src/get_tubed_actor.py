from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from src.constants import ROTATION_X


def get_tubed_actor(output_port: vtkAlgorithmOutput, radius: int, color_name: str):
    colors = vtkNamedColors()

    tube_filter = vtkTubeFilter()
    tube_filter.SetInputConnection(output_port)
    tube_filter.SetNumberOfSides(4)
    tube_filter.SetRadius(radius)

    mapper = vtkDataSetMapper()
    mapper.SetScalarVisibility(False)
    mapper.SetInputConnection(tube_filter.GetOutputPort())

    actor = vtkActor()
    actor.RotateX(ROTATION_X)
    actor.GetProperty().SetColor(colors.GetColor3d(color_name))  # type: ignore
    actor.SetMapper(mapper)

    return actor
