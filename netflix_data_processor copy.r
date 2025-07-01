library(png)
library(grid)

# Load the PNG image created by the python file - netflix_data_processor.py
img <- readPNG("ratings_dist.png")

# Display using grid
grid.raster(img)

