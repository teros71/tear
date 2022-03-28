#!/bin/bash

input=$1
output=$2
# size is height in mm
size=$3

inkscape=/Applications/Inkscape.app/Contents/MacOS/inkscape
DPI=300
PPM=$(bc <<< "($DPI*1000)/25.4")

# read background colour, width and height from svg
svghead=`head -n1 $input`
bg=$(echo $svghead | sed 's/^.*background-color:\(#[^"]*\).*$/\1/')
svg_width=$(echo $svghead | sed 's/^.*width="\([^"]*\).*$/\1/')
svg_height=$(echo $svghead | sed 's/^.*height="\([^"]*\).*$/\1/')

# how many pixels
height=$(bc <<< "$size*300/25.4")
width=$(bc <<< "$height * $svg_width / $svg_height")

echo "svg: $svg_width x $svg_height background colour $bg"
echo "png: $width x $height"

# make svg -> png using inkscape
echo "convert with inkscape"
$inkscape -o $output --export-type=png -b "$bg" -C -w $width -h $height $input

# tweak 300dpi png header, because the inkscape sets it with the assumption
# that the original is 96dpi and calculates it from image height and width
# accordingly. But we want it to be exact since we have to give the exact
# pixel size of the image, and we don't really care what was the svg height
# and width, BECAUSE IT'S SUPPOSE TO BE TOTALLY SCALABLE!
echo "set dpi=$DPI ($PPM ppm) with exiftool"
#DPI300_PPM=11811
exiftool -PixelsPerUnitX=$PPM -PixelsPerUnitY=$PPM $output
