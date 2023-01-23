from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import vtkActor, vtkRenderer


def build_renderer(actors: tuple[vtkActor, ...]):
    renderer = vtkRenderer()
    for actor in actors:
        renderer.AddActor(actor)

    colors = vtkNamedColors()
    renderer.SetBackground(colors.GetColor3d("Gray"))  # type: ignore

    return renderer
