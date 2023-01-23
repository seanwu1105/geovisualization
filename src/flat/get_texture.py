from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import vtkTexture


def get_texture(filename: str):
    reader = vtkJPEGReader()
    reader.SetFileName(filename)

    texture = vtkTexture()
    texture.SetInputConnection(reader.GetOutputPort())

    return texture
