## ----setup, include=FALSE------------------------------------------------------------------------
knitr::opts_chunk$set(echo = TRUE, warnings = FALSE, purl = FALSE)
options(warn=-1)

## ----load.package--------------------------------------------------------------------------------
# library(devtools)
# devtools::install_github("JoshOBrien/gdalUtilities")
library(gdalUtilities)      # wrappers for GDAL utility programs that could be called from the command line, but here via `sf`
# devtools::install_github("gearslaboratory/gdalUtils")
library(gdalUtils)      # wrappers for GDAL utility programs that could be called from the command line,
library(sf)             # spatial data types -- Simple Features
library(stars)          # Spatiotemporal Arrays, Raster and Vector Data Cubes
library(dplyr)          # tidyverse data manipulation functions
library(maps)           # optional -- for boundary polygons
library(mapdata)


## ----local parameters----------------------------------------------------------------------------
wfs <- "WFS:https://maps.isric.org/mapserv?map=/map/wosis_latest.map"
layer.country = 'Argentina'
wosis.dir.name <- "./wosis_latest"
file.format = 'GPKG'
file.extension = ".gpkg"
layer.name <- "wosis_latest_profiles"

## Check drivers
drivers <- sf::st_drivers()
ix <- grep(file.format, drivers$name,  fixed=TRUE)
drivers[ix,]

## Get database info from country
profiles.info <-
  gdalUtils::ogrinfo(wfs, ro=TRUE, so=TRUE, q=FALSE,
          layer=paste("ms:", layer.name, sep=''),
          where=paste("country_name='", layer.country, "'", sep=''))

## Pull the dataset
if (!file.exists(wosis.dir.name)) dir.create(wosis.dir.name)
(dst.target.name <- paste0(wosis.dir.name,"/", layer.name, "_", layer.country, file.extension))
if (!file.exists(dst.target.name)) { 
system.time(
  gdalUtilities::ogr2ogr(src=wfs,
          dst=dst.target.name,
          layer=layer.name,
          f = file.format,
          where=paste("country_name='", layer.country, "'", sep=''),
          overwrite=TRUE,
          skipfailures=TRUE)
)
}
print("file size: ")
file.info(dst.target.name)$size/1024/1024

## Convert the dataset to R dataframe
profiles.gpkg <- sf::st_read(dst.target.name)
class(profiles.gpkg)
dim(profiles.gpkg)
names(profiles.gpkg)