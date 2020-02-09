# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
env.workspace = "C:/Fire/data"

# Set local variables
inRaster = Raster("aspect")
inConstant = Raster("slope")

# Execute Times
outTimes = inRaster * inConstant

# Save the output
outTimes.save("aspectAndSlope")
