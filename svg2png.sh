#!/bin/bash

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -f|--fit)
      SIZE_SPEC="$2"
      shift # past argument
      shift # past value
      ;;
    -s|--size)
      SIZE_MM="$2"
      shift # past argument
      shift # past value
      ;;
    -t|--trial)
      TRIAL=1
      shift
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

input=$1
output=$2
if [ -n "$SIZE_SPEC" ]; then
  case $SIZE_SPEC in
    A4)
      SIZE_MM=210
      SIZE_MAX=297
      ;;
    A3)
      SIZE_MM=297
      SIZE_MAX=420
      ;;
    A2)
      SIZE_MM=420
      SIZE_MAX=594
      ;;
    A1)
      SIZE_MM=594
      SIZE_MAX=841
      ;;
    A0)
      SIZE_MM=841
      SIZE_MAX=1189
      ;;
    *)
      echo "unknown size spec"
      exit 1
      ;;
  esac
fi

if [ -z "$SIZE_MM" ]; then
  echo "missing size"
  exit 1
fi

inkscape=/Applications/Inkscape.app/Contents/MacOS/inkscape
DPI=300
PPM=$(bc <<< "($DPI*1000)/25.4")

# read background colour, width and height from svg
svghead=`head -n1 $input`
bg=$(echo $svghead | sed 's/^.*background-color:\(#[^"]*\).*$/\1/')
svg_width=$(echo $svghead | sed 's/^.*width="\([^"]*\).*$/\1/')
svg_height=$(echo $svghead | sed 's/^.*height="\([^"]*\).*$/\1/')

if (( svg_width > svg_height )); then
  svg_short=$svg_height
  svg_long=$svg_width
else
  svg_short=$svg_width
  svg_long=$svg_height
fi

# size is in mm, and is the shorter side of the paper
# whether the image is a portrait or landscape will be then
# decided by the image width and height

size=$SIZE_MM

if [ -n "$SIZE_MAX" ]; then
  svg_ratio=$(bc -l <<< "$svg_long / $svg_short")
  if (( $(bc <<< "$svg_ratio > sqrt(2)") )); then
    size=$(bc <<< "$SIZE_MAX / $svg_ratio")
  fi
fi

# how many pixels
short_side=$(bc <<< "$size*300/25.4")
if (( svg_width > svg_height )); then
  # landscape
  height=$short_side
  width=$(bc <<< "$height * $svg_width / $svg_height")
else
  # portrait
  width=$short_side
  height=$(bc <<< "$width * $svg_height / $svg_width")
fi

echo "svg: $svg_height x $svg_width background colour $bg"
echo "png: $height x $width"

# make svg -> png using inkscape
echo "convert with inkscape"
if [ -z "$TRIAL" ]; then
  $inkscape -o $output --export-type=png -b "$bg" -C -w $width -h $height $input
fi

# tweak 300dpi png header, because the inkscape sets it with the assumption
# that the original is 96dpi and calculates it from image height and width
# accordingly. But we want it to be exact since we have to give the exact
# pixel size of the image, and we don't really care what was the svg height
# and width, BECAUSE IT'S SUPPOSE TO BE TOTALLY SCALABLE!
echo "set dpi=$DPI ($PPM ppm) with exiftool"
#DPI300_PPM=11811
year=$(date +%Y)
if [ -z "$TRIAL" ]; then
  exiftool -Software="TeArt" -Artist="Tero Suomela" -Copyright="$year Tero Suomela" -PixelsPerUnitX=$PPM -PixelsPerUnitY=$PPM $output
fi
