# Assignment 1: Geovisualization

## Objectives

In this first project, you will familiarize yourself with VTK while
experimenting with several visualization techniques for 2D scalar data. The
topic here is geovisualization, in other words, the visualization of geographic
data. You will visualize a dataset that combines bathymetry/topography data (see
below for definitions) with satellite imagery of the Earth's surface. In
addition, your visualization will include a graphical user interface (aka GUI)
that interactively controls certain visualization features.

## Background

Bathymetry measures the underwater depth of the ocean floor, while topography
measures land elevation with respect to sea level. Together, they describe the
Earth's surface’s geometry. For simplicity, I use the term elevation in the
following to refer to both.
[NASA’s Blue Marble project](https://visibleearth.nasa.gov/collection/1484/blue-marble)
offers high-resolution elevation datasets and satellite imagery of the Earth's
surface, acquired at different times of the year. In this project, you will
learn how to use VTK to create impressive interactive visualizations of the
elevation data.

The data consists of gray-scale images
([relief](https://visibleearth.nasa.gov/images/73963/bathymetry)/[topography](https://visibleearth.nasa.gov/images/73934/topography))
and color images
([satellite views](https://visibleearth.nasa.gov/images/73776/august-blue-marble-next-generation-w-topography-and-bathymetry))
with resolutions up to 86400 x 43200 (3.7 gigapixels). In each image, the
Earth's surface is sampled at regular angular intervals spanning the domain
`[−π,π]×[−π/2,π/2]` in spherical coordinates, i.e., longitude/latitude (see
illustration below).

Each row of the image corresponds to a parallel (line of constant latitude,
shown in red), while each column corresponds to a meridian (line of constant
longitude, shown in blue). Note that the North and South poles (where parallels
are points) are each represented by an entire row of uniform value.

## Task 1. Height Map Visualization and Texture Mapping (50%)

### Task summary

Your first task is to visualize the elevation dataset through an interactive
height map textured with the satellite image. See explanations below.

### Height map

A height map is a representation of a gray-scale (scalar) image through a curved
surface, whereby the pixel (x,y) associated with value f in the image is mapped
to the 3D position (x,y,f): f becomes the z-coordinate. In the case of the
elevation dataset, the resulting surface matches (by definition) the Earth's
elevation profile.

Computing a height map in VTK can be done with the help of the
[vtkWarpScalar](https://vtk.org/doc/nightly/html/classvtkWarpScalar.html)
filter, whose basic usage is demonstrated in ImageWarp.py (found
[here](https://kitware.github.io/vtk-examples/site/Cxx/Images/ImageWarp/)).

### Interactivity

vtkWarpScalar provides a scale factor that controls the amount by which the
image is moved up or down for a given scalar value at each point: {(x,y),f} is
mapped to (x,y, Kf) by the algorithm, where K is the scale factor. This control
mechanism can be tied to a slider GUI to permit the interactive manipulation of
the scale factor and update the visualization accordingly.

### Texture mapping

Height mapping, as described previously, produces a geometric representation of
the Earth’s surface. In the absence of additional visual cues, however, key
aspects of the data, such as the continents’ coastlines, remain ambiguous. To
remedy this problem, you will use the available satellite image through texture
mapping. Here, texture mapping refers to wrapping a geometric object with an
image.

In VTK, textures are stored in
[vtkTexture](https://vtk.org/doc/nightly/html/classvtkTexture.html) objects that
can then be supplied to
[vtkActor](https://vtk.org/doc/nightly/html/classvtkActor.html) to enable
texture mapping during the rendering stage. Note that this mapping is only
possible if the vertices of the target geometry (here, the height surface) are
equipped with texture coordinates that specify their matching location on the
texture. Fortunately, this information is already included in the elevation
datasets I am giving you.

### Implementation

You will write for this task a small program that satisfies the following
requirements:

- Import the necessary files (elevation and satellite image) using the
  appropriate VTK readers.
- Compute a height map representation of the elevation with vtkWarpScalar.
- Texture map the satellite image onto the height map geometry.
- Visualize the result.
- Provide a slider bar GUI to manipulate the scale factor of vtkWarpScalar
  interactively
- Maintain consistency between visualization and GUI.

### API

Your program will have the following API:

```sh
python heightfield.py [-g|--geometry] <elevation> [-i|--image] <image>
```

where `<elevation>` is the path of the elevation data file, and `<image>` is the
path of the satellite picture. The parsing of this API is most easily achieved
using argparse.

### Report

- Include in your report images of the visualization results produced by your
  program.
- Make sure to select camera angles that convey the presence of a 3rd dimension.
- Provide several images showing the results obtained for different scale
  factors.
- Include close-up images.

## Task 2. Isocontours (20%)

### Task summary

For the second task, you will visualize the elevation dataset using isocontours.

### Isocontours

One needs [isocontours](https://en.wikipedia.org/wiki/Contour_line), also known
as contour lines, isolines, or, more formally, level sets to highlight specific
elevation values. An isocontour corresponds to the set of points where the
considered function has a particular value (the pre-image of that function at
that value). In 2D, isocontours form closed curves. Note that we will study this
topic in great detail when we consider isosurfaces in the coming weeks. By
selecting a number of discrete values between the minimum and the maximum values
of the data set, one can get a good illustration of the value distribution
across the domain. To compute isocontours in the elevation dataset, you will use
[vtkContourFilter](https://vtk.org/doc/nightly/html/classvtkContourFilter.html),
the API of which is discussed
[here](https://vtk.org/doc/nightly/html/classvtkContourFilter.html#details).

Specifically, you will create a visualization that shows isocontours associated
with elevation values ranging from -10,000 meters to +8,000 meters in 1,000
meters increments. To improve the clarity of your visualization, you will wrap
the isocontour into tubes using
[vtkTubeFilter](https://vtk.org/doc/nightly/html/classvtkTubeFilter.html#details).
Note that the radius of your tubes must be selected carefully (not too big to
avoid occlusion and not too small to make them easily distinguishable). The sea
level itself (elevation 0) will be shown in red.

To provide context to the isocontours, you will apply the same texture mapping
solution as in the previous task, this time however to a flat geometry. Select
colors for your isolines that contrast nicely with the underlying satellite
image.

### Implementation

You will write for this task a program that meets the following requirements:

- Import the elevation dataset and satellite using the appropriate VTK readers.
- Define a vtkContourFilter to create a series of isocontours in 1,000 meters
  increments in the interval -10,000 meters to +8,000 meters (19 values).
- Display the resulting curves as tubes using vtkTubeFilter.
- Color the tubes using properly selected colors.
- Texture map a satellite image to the dataset.

### API

The API for your program should be as follows:

```sh
python isocontour.py [-g|--geometry] <elevation> [-i|--image] <image>
```

where `<elevation>` is the path of the elevation data file and `<image>` is the
path of the satellite picture.

### Report

- Include in your report high-quality images of the results produced by your
  program.
- Include close-up images.

## Task 3. Complete Visualization on a Sphere (20%)

### Task summary

For this third and final task, you will integrate height field representation,
texture mapping, and isocontours and display them on a sphere to create a nice
visualization of the elevation dataset.

### Interactive scalar field visualization

The third task in this project consists in combining the various visualization
techniques that you implemented previously in a single visualization.
Specifically, you should write a program that displays the elevation dataset as
a height field, applies satellite imagery to it using texture mapping (as done
in Task 1), and visualizes isocontours as tubes (cf. Task 2). In addition, as
discussed previously, your visualization should include a slider bar to control
the scaling factor of the height field representation.

### Mapping to a sphere

In contrast to what you have done so far, you will display height field,
texture, and isocontours on a sphere instead of a plane. Indeed, the results
achieved so far do not convey the actual shape of the various continents due to
the significant distortion caused by the image's latitude/longitude
parameterization (a long-standing problem in cartography!). Therefore, we need
to visualize the data directly on a sphere to remedy this problem.

To make your task easier, I am providing you with a sphere dataset that contains
elevation values, normals, and texture coordinates. Note that the sphere I am
giving you is already scaled to the radius of the Earth (in meters).

### Implementation

You will write for this task a program that satisfies the following
requirements:

- Import the elevation dataset on a sphere and satellite image using the
  appropriate VTK readers.
- Apply vtkWarpScalar to visualize the elevation data as a height field.
- Provide a slider bar to control the scaling factor of vtkWarpScalar.
- Texture map the satellite image onto the height field.
- Apply vtkContourFilter to create a series of isocontours in 1,000 meters
  increments in the interval -10,000 meters to +8,000 meters.
- Display the resulting curves as tubes using vtkTubeFilter.
- Draw the tubes directly on the height field.
- Keep visualization and slider GUI selection consistent.

### API

The API for your program should be as follows:

```
python view_earth.py [-g|--geometry] <sphere_elevation> [-i|--image] <image>
```

where `<sphere_elevation>` is the path of the elevation on a sphere data file
and `<image>` is the path of the satellite image.

### Report

- Include in your report high-quality images of the results produced by your
  program.
- Provide images showing the results obtained for several scaling factors.
- Include images that show different parts of the world and different
  perspectives.
- Include comparisons with and without contours for the same geographical areas.
- Include close-up images.

## Discussion (10%)

Answer the following questions in your report. Be as specific as possible and
draw from your experience in this assignment to justify your opinion.

Considering the height map technique used in Task 1:

1. Which properties of the dataset were effectively visualized with this
   technique?
1. What are, in your opinion, the main limitations of this technique, and how
   could you address them?
1. How useful did you find the slider interface in your usage of the height
   field representation?
1. How effective do you find this visualization technique for this dataset?

Considering the level sets considered in Task 2:

- Which specific aspects of the data were readily visible with isocontours?

Considering the sphere representation in Task 3:44

1. What benefits did you see to the perform the visualization on a sphere?
1. How did the resulting visualization compare to the previous ones?

Considering your findings in tasks 1, 2, and 3:

- Did you find that the combined use of these visualization techniques in Task 3
  improved the results of each method applied separately? Why or why not?

## Datasets

As indicated in the preamble, the data used in this project is courtesy of NASA
Earth Observatory and is available on the website of the
[Blue Marble project](https://visibleearth.nasa.gov/collection/1484/blue-marble).
Since the server can sometimes be slow, I am providing you with a local copy of
the relevant files. Note that I converted the bathymetry/topography datasets to
a single vtkImageData to simplify your programs. The dataset is available in 4
different resolutions for convenience. Similarly, the satellite image of the
Earth is provided in 3 different resolutions. In both cases, use a
low-resolution version to test your implementation and use the highest
resolution that your program and your computer can handle in your report. Note
that some of these files are large (see below), so download only what you need.
