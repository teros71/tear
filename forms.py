"""For storing forms"""

from xml.dom import minidom
import copy

import default
import shape
from geometry import geom

form_table = {}
image_table = {}
clip_table = []

man = "22.574 241.670, 22.573 237.260, 21.007 229.560, 19.525 207.020, 18.043 187.610, 15.842 186.440, 16.049 154.770, 16.145 120.480, 11.556 113.190, 3.437 102.000, 0.364 89.800, 1.490 76.109, 6.639 47.671, 11.330 45.586, 30.796 32.788, 29.758 26.686, 30.623 8.425, 44.112 2.197, 54.637 7.163, 53.092 21.952, 52.038 28.059, 58.366 39.609, 70.450 46.217, 75.082 58.513, 82.259 82.699, 82.080 93.109, 80.506 102.090, 78.053 107.800, 76.034 111.990, 71.913 118.170, 69.034 119.660, 69.034 132.690, 69.983 152.420, 71.394 171.990, 69.601 186.990, 65.920 210.910, 64.978 223.180, 63.762 228.770, 67.898 236.340, 59.705 242.610, 47.375 242.610, 48.381 237.060, 47.977 226.310, 46.551 205.410, 45.421 188.600, 40.921 188.360, 37.534 189.230, 36.746 202.170, 36.981 221.060, 36.576 229.190, 34.841 236.740, 34.534 242.110, 28.873 242.410, 22.574 241.670"

dancer = "254.375 641.057, 243.246 641.126, 235.905 638.999, 235.757 629.063, 236.193 612.796, 236.142 602.937, 237.120 599.359, 238.334 588.826, 238.315 583.770, 240.024 578.262, 240.632 564.063, 239.115 554.045, 237.551 548.576, 235.150 529.375, 234.439 523.125, 234.452 504.531, 234.304 498.346, 225.254 497.853, 219.554 496.123, 216.043 494.986, 213.644 494.313, 213.088 495.047, 210.250 495.743, 206.759 495.196, 205.079 494.688, 202.187 493.594, 197.387 492.500, 191.645 491.382, 183.534 487.165, 181.082 485.625, 177.401 482.422, 170.121 476.348, 167.303 474.004, 164.027 470.625, 161.038 467.446, 155.937 461.040, 149.080 451.875, 144.705 445.672, 141.959 441.922, 139.998 439.178, 137.726 435.394, 133.612 428.662, 129.215 420.267, 124.897 412.344, 122.023 407.031, 115.625 394.844, 110.591 380.938, 108.414 374.518, 107.503 371.237, 105.743 360.646, 104.914 357.365, 103.135 351.835, 102.637 349.845, 101.683 344.416, 100.619 338.281, 98.014 331.329, 97.150 327.735, 96.220 323.692, 95.625 321.093, 95.280 319.315, 94.692 317.069, 93.185 310.625, 91.583 302.188, 90.906 295.156, 91.563 277.500, 92.183 272.948, 92.944 268.729, 93.743 264.338, 94.561 259.651, 96.566 249.531, 98.748 234.375, 101.579 223.982, 102.667 220.017, 98.623 217.517, 81.327 202.723, 71.597 185.259, 66.201 174.004, 60.938 165.899, 50.289 153.769, 46.849 152.882, 44.105 152.382, 42.821 151.963, 40.233 151.532, 36.935 150.606, 32.548 146.460, 30.764 135.769, 32.242 129.466, 32.656 126.593, 31.295 121.484, 29.676 118.750, 29.205 118.047, 28.266 116.563, 27.229 114.958, 24.677 113.255, 19.733 109.451, 16.661 105.659, 14.224 103.776, 8.153 97.496, 9.284 93.267, 13.708 93.996, 20.603 96.253, 24.190 96.722, 27.003 97.192, 33.914 99.880, 43.885 106.142, 52.699 113.821, 56.588 118.596, 60.235 123.293, 64.190 128.434, 67.847 133.237, 74.889 142.836, 78.906 147.482, 89.287 157.388, 121.431 189.198, 124.415 192.792, 126.073 194.737, 127.595 196.222, 132.656 199.520, 139.019 203.816, 145.018 207.822, 146.780 209.528, 158.400 217.224, 167.775 225.181, 175.469 231.504, 180.156 233.744, 185.156 236.907, 189.780 241.454, 191.254 243.507, 197.966 247.508, 200.664 249.984, 208.125 255.804, 211.320 257.741, 214.086 257.988, 217.187 256.519, 217.656 254.483, 218.125 252.452, 218.584 250.444, 220.926 231.719, 220.509 221.696, 219.518 205.937, 227.503 188.746, 229.301 185.983, 230.529 183.697, 231.562 181.287, 232.217 180.297, 232.871 179.947, 232.197 179.229, 231.933 174.646, 231.848 140.469, 231.249 135.625, 230.405 129.844, 231.727 76.836, 232.187 70.035, 238.418 57.187, 256.243 40.156, 270.444 27.844, 274.714 24.250, 278.084 21.406, 281.558 18.594, 284.839 15.943, 288.641 12.429, 296.005 9.048, 300.772 9.050, 305.049 10.153, 310.158 11.894, 317.797 14.819, 325.781 18.883, 329.640 21.858, 334.865 28.125, 337.168 32.263, 338.069 34.763, 334.725 36.415, 329.816 32.004, 328.180 30.764, 330.133 33.748, 332.187 36.437, 331.347 38.211, 330.872 41.167, 329.595 44.941, 326.043 43.730, 324.582 42.977, 322.858 43.438, 318.247 38.326, 316.745 35.381, 315.704 35.939, 314.040 36.335, 309.498 32.135, 307.563 30.345, 300.983 25.973, 297.250 25.437, 290.083 32.972, 285.864 38.077, 283.205 41.468, 280.690 44.797, 278.666 47.500, 275.400 51.780, 270.625 58.115, 265.156 65.308, 262.677 68.400, 260.005 71.563, 255.316 90.000, 254.678 103.994, 254.455 111.182, 257.913 121.621, 262.191 141.129, 264.480 149.349, 266.360 151.956, 267.429 152.277, 273.141 146.250, 276.082 141.986, 278.444 135.469, 279.841 129.219, 280.446 123.671, 279.968 121.387, 279.688 121.700, 278.188 121.813, 278.594 118.125, 279.375 114.681, 281.224 106.719, 283.288 99.863, 284.357 96.894, 285.449 93.906, 288.969 87.847, 291.270 84.648, 293.191 82.779, 295.387 81.223, 297.359 80.036, 299.718 78.726, 303.388 77.478, 307.522 76.849, 311.741 77.111, 322.708 81.242, 329.909 85.864, 335.001 94.219, 335.618 96.406, 336.777 101.650, 333.138 115.461, 332.811 116.659, 331.410 120.622, 329.050 126.977, 324.198 137.344, 321.947 140.938, 320.910 148.438, 319.929 156.509, 318.472 159.261, 317.813 160.071, 317.370 160.913, 317.683 163.651, 318.125 166.718, 317.813 170.603, 316.355 178.721, 315.531 180.411, 317.082 181.846, 320.020 184.317, 332.171 192.361, 342.813 200.196, 350.019 210.171, 352.512 214.531, 362.287 223.871, 370.528 231.198, 382.554 241.907, 385.120 245.247, 388.307 249.329, 390.796 252.972, 390.946 256.045, 389.688 261.774, 382.946 278.600, 381.573 281.673, 378.223 286.726, 372.495 290.071, 370.000 291.299, 365.313 293.072, 355.156 295.478, 349.973 296.645, 346.977 297.421, 342.405 296.374, 335.558 294.454, 333.180 292.708, 333.604 291.034, 331.719 289.190, 327.544 285.825, 334.531 281.864, 348.125 283.102, 351.668 280.688, 354.885 276.925, 356.734 274.545, 357.012 272.659, 351.793 272.193, 342.980 267.136, 346.197 265.625, 357.091 263.028, 362.350 262.012, 365.545 264.071, 367.822 265.932, 367.512 256.799, 367.124 254.692, 363.015 252.451, 355.532 248.152, 338.752 237.474, 332.659 232.150, 321.980 223.421, 315.021 225.104, 310.095 227.046, 306.875 229.279, 304.844 234.809, 302.813 240.329, 302.402 241.225, 301.480 242.969, 295.506 255.580, 292.813 264.090, 291.553 267.130, 290.271 272.082, 288.744 282.812, 287.448 296.549, 287.481 298.505, 287.647 308.955, 288.918 342.812, 288.942 359.531, 290.106 371.406, 296.872 464.687, 298.063 494.378, 291.929 496.113, 286.562 496.886, 281.562 497.495, 273.281 499.512, 271.797 500.480, 270.936 503.393, 269.669 518.594, 266.207 535.616, 263.426 549.835, 261.874 560.625, 260.193 577.031, 260.903 585.373, 261.265 590.361, 259.971 594.119, 259.074 598.975, 260.456 606.875, 262.482 616.890, 264.347 624.741, 265.625 629.245, 266.901 633.333, 267.788 636.981, 258.984 640.385, 255.625 641.156, 255.000 641.562, 254.375 641.057"

standing_man = "101.690 351.870, 101.530 347.430, 101.980 342.700, 102.760 342.130, 102.070 340.990, 101.050 338.470, 100.900 334.060, 100.740 331.140, 99.849 331.140, 98.958 331.140, 97.128 326.260, 94.224 315.350, 93.086 261.770, 93.194 249.170, 84.314 227.560, 78.130 215.200, 77.286 221.370, 76.947 267.530, 76.937 279.410, 77.406 287.050, 77.894 292.450, 79.809 302.700, 84.149 320.710, 83.245 329.660, 82.736 332.370, 81.282 333.790, 79.827 335.210, 79.728 338.390, 79.302 342.070, 79.180 343.290, 79.432 346.510, 79.914 349.510, 80.625 350.520, 80.115 350.900, 79.152 350.490, 78.972 350.650, 77.468 350.940, 72.607 350.820, 68.767 350.840, 62.289 350.590, 61.861 351.010, 61.620 351.110, 60.465 350.950, 59.845 350.890, 57.535 350.400, 54.664 349.610, 54.244 348.660, 53.475 346.980, 52.695 343.900, 52.683 342.060, 54.113 340.260, 56.931 336.990, 59.154 332.170, 59.036 324.400, 56.499 316.970, 54.940 315.010, 54.296 299.460, 53.167 282.280, 52.567 276.400, 51.953 270.530, 51.613 266.210, 50.802 260.210, 47.866 249.260, 44.604 237.370, 41.444 225.640, 41.406 221.080, 41.368 216.520, 38.104 216.370, 34.610 216.070, 32.130 215.580, 27.095 213.690, 24.703 210.340, 22.053 205.080, 21.416 200.520, 21.537 198.400, 20.501 198.400, 19.466 198.400, 19.334 197.380, 18.830 192.030, 18.361 186.990, 17.874 182.670, 17.412 178.470, 16.791 170.430, 16.403 163.430, 16.352 149.190, 16.906 144.860, 17.408 140.660, 18.474 111.540, 20.379 94.814, 21.930 89.997, 30.719 85.254, 52.755 74.221, 53.592 71.266, 52.860 67.635, 50.643 61.677, 49.383 59.551, 47.891 58.593, 46.078 51.323, 46.644 48.918, 47.374 45.063, 50.065 32.969, 55.554 28.201, 63.435 26.115, 77.877 31.221, 81.108 37.255, 81.816 43.877, 82.414 49.221, 82.813 54.351, 81.435 58.036, 79.224 63.179, 78.612 66.463, 79.520 71.843, 87.611 76.469, 101.650 80.149, 113.300 83.860, 117.510 93.494, 118.960 100.820, 120.730 112.700, 123.610 129.740, 124.720 136.150, 125.240 148.870, 125.150 158.430, 122.820 172.080, 120.500 185.810, 119.150 185.960, 117.790 186.030, 117.800 187.350, 117.970 191.910, 117.120 202.000, 120.230 222.400, 121.570 229.960, 122.300 234.040, 123.860 247.370, 124.600 254.090, 124.820 314.260, 123.600 319.290, 122.660 323.280, 122.020 327.220, 120.600 330.080, 120.020 331.270, 120.850 333.430, 125.850 338.620, 127.940 344.150, 126.830 346.640, 124.820 347.800, 120.660 349.880, 119.570 350.830, 118.860 351.110, 118.580 350.990, 117.900 350.870, 117.620 350.880, 116.980 350.840, 116.220 350.950, 116.420 350.830, 116.610 350.700, 115.850 350.810, 115.210 350.760, 114.970 350.830, 114.560 350.950, 111.580 350.890, 110.680 350.840, 109.230 350.790, 108.360 350.800, 107.920 350.810, 105.210 350.750, 104.360 350.800, 103.380 350.790, 102.530 350.810, 101.890 350.880, 101.830 351.370, 101.690 351.870"

sitting_shape = "47.045 295.574, 48.470 210.989, 76.507 178.200, 83.160 138.283, 88.387 134.957, 86.962 118.325, 95.990 107.395, 106.920 116.899, 116.899 140.184, 100.267 115.474, 95.515 116.424, 99.792 118.325, 95.515 131.630, 100.267 133.056, 105.019 167.746, 91.238 209.563, 108.346 295.099"


class Image:
    def __init__(self, name, paths):
        self.name = name
        self.paths = paths
        self.type = "mask"

    @classmethod
    def fromfile(cls, name, fname):
        # parse an xml file by name
        file = minidom.parse(fname)
        # use getElementsByTagName() to get tag
        paths = file.getElementsByTagName('path')
        # one specific item attribute
        pds = [p.attributes['d'].value for p in paths]
        return cls(name, pds)


def init():
    """initialize forms"""
    def add_poly(name, pl):
        p = geom.Polygon.fromstr(pl)
        bb = p.bbox(geom.Point(0, 0))
        p.move(-(bb.x0 + (bb.x1 - bb.x0) / 2), -(bb.y0 + (bb.y1 - bb.y0) / 2))
        add(name, shape.Shape(p))
    add_poly("man", man)
    add_poly("dancer", dancer)
    add_poly("standing-man", standing_man)
    add_poly("sitting-shape", sitting_shape)

    add_image("umbrella", Image.fromfile("umbrella", "images/1538174796.svg"))


def get(name):
    s = form_table.get(name)
    if s is not None:
        return copy.deepcopy(s)
    return None


def add(name, form):
    print(f"added form {name}")
    form_table[name] = form


def get_image(name):
    return image_table.get(name)


def add_image(name, img):
    print(f"added image {name}")
    image_table[name] = img


def add_clip(name):
    clip_table.append(name)
    return f'clip_{len(clip_table)}'
