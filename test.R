## ----setup, include=FALSE------------------------------------------------------------------------
knitr::opts_chunk$set(echo = TRUE, warnings = FALSE, purl = FALSE)
options(warn=-1)


## ----load.package--------------------------------------------------------------------------------
# library(devtools)
# devtools::install_github("JoshOBrien/gdalUtilities")
library(gdalUtilities)      # wrappers for GDAL utility programs that could be
                        #  called from the command line, but here via `sf`
# devtools::install_github("gearslaboratory/gdalUtils")
library(gdalUtils)      # wrappers for GDAL utility programs that could be
                        #  called from the command line,
library(sf)             # spatial data types -- Simple Features
library(stars)          # Spatiotemporal Arrays, Raster and Vector Data Cubes
library(dplyr)          # tidyverse data manipulation functions
library(ggplot2)        # gpplot graphics
library(maps)           # optional -- for boundary polygons
library(mapdata)


## ------------------------------------------------------------------------------------------------
drivers <- sf::st_drivers()
# print(drivers)
ix <- grep("GPKG", drivers$name,  fixed=TRUE)
drivers[ix,]
ix <- grep("ESRI", drivers$name,  fixed=TRUE)
drivers[ix,]
ix <- grep("CSV", drivers$name,  fixed=TRUE)
drivers[ix,]

wfs <- "WFS:https://maps.isric.org/mapserv?map=/map/wosis_latest.map"

india.profiles.info <-
  gdalUtils::ogrinfo(wfs, ro=TRUE, so=TRUE, q=FALSE,
          layer="ms:wosis_latest_profiles",
          where="country_name='India'")


wosis.dir.name <- "./wosis_latest"
if (!file.exists(wosis.dir.name)) dir.create(wosis.dir.name)

wosis.dir.name.india <- "./wosis_latest/india"
if (!file.exists(wosis.dir.name.india)) dir.create(wosis.dir.name.india)
layer.name <- "ms_wosis_latest_profiles"
(dst.target.name <- paste0(wosis.dir.name,"/", layer.name, ".shp"))
if (!file.exists(dst.target.name)) { 
  system.time(
  gdalUtilities::ogr2ogr(src=wfs,
          dst=wosis.dir.name.india,
          layer=layer.name,
          f = "ESRI Shapefile",
          where="country_name='India'",
          overwrite=TRUE,
          skipfailures=FALSE)
)
}

profiles.india <- sf::st_read(dsn=wosis.dir.name.india, layer=layer.name,
                stringsAsFactors = FALSE)
dim(profiles.india)
names(profiles.india)
head(profiles.india)