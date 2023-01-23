# Geovisualization

CS530 Introduction to Scientific Visualization assignment 1 @Purdue.

## Getting Started

Install Python 3.11.1 or later.

Install Poetry **1.3.2 or later**. See
[Poetry's documentation](https://python-poetry.org/docs/) for details.

> Poetry earlier than 1.3 will not work.

Install the project's dependencies:

```sh
poetry install --no-root
```

Activate the virtual environment:

```sh
poetry shell
```

Execute the application:

```sh
python heightfield.py [-g|--geometry] <elevation> [-i|--image] <image>
```

where `<elevation>` is the path of the elevation data file, and `<image>` is the
path of the satellite picture.

```sh
python isocontour.py [-g|--geometry] <elevation> [-i|--image] <image>
```

where `<elevation>` is the path of the elevation data file and `<image>` is the
path of the satellite picture.

```sh
python view_earth.py [-g|--geometry] <sphere_elevation> [-i|--image] <image>
```

where <sphere_elevation> is the path of the elevation on a sphere data file and
<image> is the path of the satellite image.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
