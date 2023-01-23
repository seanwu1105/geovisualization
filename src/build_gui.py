from typing import Callable

from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QMainWindow, QSlider, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


def build_gui(
    elevation_mapper_filename: str,
    texture_filename: str,
    build_vtk_widget: Callable[
        [QObject, str, str], tuple[QVTKRenderWindowInteractor, Callable[[int], None]]
    ],
    default_scale: int,
):
    window = QMainWindow()
    window.resize(640, 480)
    central = QWidget()
    layout = QGridLayout()

    vtk_widget, on_scale_changed = build_vtk_widget(
        central, elevation_mapper_filename, texture_filename
    )
    layout.addWidget(
        vtk_widget,
        0,
        0,
        1,
        -1,
    )
    layout.addWidget(QLabel("Scale"), 1, 0)

    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setMinimum(1)
    slider.setMaximum(default_scale * 2)
    slider.setValue(default_scale)
    slider.valueChanged.connect(on_scale_changed)  # type: ignore
    layout.addWidget(slider, 1, 1)

    central.setLayout(layout)
    window.setCentralWidget(central)
    return window
