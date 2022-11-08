suppressPackageStartupMessages(library(argparse))

parser <- ArgumentParser()
parser$add_argument("country",
    help = "Available country areas to get profiles from: Argentina, Uruguay, Chile")
parser$add_argument("format",
    help = "Available formats: CSV, GPKG, SHP")
parser$add_argument("property",
    help = "Available properties: clay, bdfi33, orgc, profiles")
parser$add_argument("-v", "--verbose", action="store_true", default=FALSE,
    help="Print extra output [default]")
parser$add_argument("-q", "--quietly", action="store_false", 
    dest="verbose", help="Print little output")
                                        
# get command line options, if help option encountered print help and exit,
# otherwise if options not found on command line then set defaults, 
args <- parser$parse_args()

## ----setup, include=FALSE------------------------------------------------------------------------
knitr::opts_chunk$set(echo = TRUE, warnings = FALSE, purl = FALSE)
options(warn=-1)

## ----load.package--------------------------------------------------------------------------------
# library(devtools)
# devtools::install_github("JoshOBrien/gdalUtilities")
suppressPackageStartupMessages(library(gdalUtilities))      # wrappers for GDAL utility programs that could be called from the command line, but here via `sf`
# devtools::install_github("gearslaboratory/gdalUtils")
suppressPackageStartupMessages(library(gdalUtils))      # wrappers for GDAL utility programs that could be called from the command line,
suppressPackageStartupMessages(library(sf))             # spatial data types -- Simple Features
suppressPackageStartupMessages(library(stars))          # Spatiotemporal Arrays, Raster and Vector Data Cubes
suppressPackageStartupMessages(library(dplyr))          # tidyverse data manipulation functions
suppressPackageStartupMessages(library(maps))           # optional -- for boundary polygons
suppressPackageStartupMessages(library(mapdata))


## ----local parameters----------------------------------------------------------------------------
layer.country = args$country
file.format = args$format
layer.type = args$property

## ---- other local variables. Do not modify ------------------------------------------------------
wfs <- "WFS:https://maps.isric.org/mapserv?map=/map/wosis_latest.map"
wosis.dir.name <- "./wosis_latest"
layer.name <- paste("wosis_latest_", layer.type, sep="")


file.extension = paste(".", tolower(file.format), sep="")
if (file.format == 'SHP'){
    file.format = 'ESRI Shapefile'
}

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