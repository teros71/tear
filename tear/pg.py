"""playground geometry definitions"""
WIDTH = 1000
HEIGHT = 1000
CENTER_X = 500
CENTER_Y = 500
GR_X0 = 700
GR_Y0 = 700
GR_X1 = 300
GR_Y1 = 300

# sizes
A0 = {"w_mm": 841, "h_mm": 1189, "w_300ppi": 9933, "h_300ppi": 14043}
A1 = {"w_mm": 594, "h_mm": 841, "w_300ppi": 7016, "h_300ppi": 9933}
A2 = {"w_mm": 420, "h_mm": 594, "w_300ppi": 4960, "h_300ppi": 7016}
A3 = {"w_mm": 297, "h_mm": 420, "w_300ppi": 3508, "h_300ppi": 4960}
A4 = {"w_mm": 210, "h_mm": 297, "w_300ppi": 2480, "h_300ppi": 3508}

SQUARE = {"w": 900, "h": 900}
LANDSCAPE_2BY3 = {"w": 1350, "h": 900}
LANDSCAPE_3BY4 = {"w": 1200, "h": 900}
LANDSCAPE_12BY15 = {"w": 1125, "h": 900}
LANDSCAPE_1BY2 = {"w": 1800, "h": 900}
PORTRAIT_3BY2 = {"h": 1350, "w": 900}
PORTRAIT_4BY3 = {"h": 1200, "w": 900}
PORTRAIT_15BY12 = {"h": 1125, "w": 900}
PORTRAIT_1BY2 = {"h": 1800, "w": 900}

# A3 in 2/3 : 280 x 420 : 3307 x 4960 (300ppi)

# what to use for svg dimensions?
# square : 1/1   : 900 x 900
# 60x90  : 2/3   : 900 x 1350
# 75x100 : 3/4   : 900 x 1200
# 60x75  : 12/15 : 900 x 1125

# in 300 dpi:
# 24" ~  60cm :  7200px ~  7086px
# 30" ~  75cm :  9000px ~  8858px
# 36" ~  90cm : 10800px ~ 10630px
# 40" ~ 100cm : 12000px ~ 11811px
# 48" ~ 122cm : 14400px ~ 14400px

# standard canvas sizes
# 18 x 24 in (45 x 60 cm)
# 20 × 24 in (50 × 60 cm)
# 24 x 30 in (60 x 75 cm)
# 24 × 36 in (60 × 90 cm)
# 30 × 30 in (75 x 75 cm)
# 30 x 40 in (75 x 100 cm)
# 36 × 36 in (90 x 90 cm)
# 36 x 48 in (90 x 122 cm)
# 40 × 40 in (100 x 100 cm)
