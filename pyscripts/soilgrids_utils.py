import rasterio
from pyproj import Transformer
from soilgrids import SoilGrids
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from country_bounding_boxes import country_subunits_by_iso_code
from pyscripts import settings
import re
import os
from os.path import exists


country_map = {
    'Argentina': 'AR',
    'Uruguay': 'UY',
    'Chile': 'CL',
    'Paraguay': 'PY'
}

def complement_bdod(country_name, download_rasters, plot):
    if download_rasters:
        get_raster_files(country_name)
    df_sgds = ponderate_soilgrids_rasters(country_name)
    df_comp = join_with_wosis_data(country_name, df_sgds)
    if plot:
        plot_raster_with_profiles(country_name)
    return df_comp

def get_raster_files(country_name):

    country_code = country_map[country_name]
    bddata = []
    bbox = list([c.bbox for c in country_subunits_by_iso_code(country_code)][0]) # returns tuple inside list
    bbox = transform_crs("epsg:4326", settings.flat_crs, bbox)

    bboxes = bbox_split_v(bbox, 2)
    for idx, bbox in enumerate(bboxes):
        for depth in ['0-5', '5-15', '15-30']:
            bddata.append(get_bulk_density(bbox, depth, f'{country_code}_{idx}'))

def ponderate_soilgrids_rasters(country_name):
    country_code = country_map[country_name]

    gdf_bd_pond = gpd.read_file(settings.wosis_dir + f"wosis_latest_profiles_{country_name}.shp").to_crs(settings.flat_crs)
    total_depth = 30

    for depth_code, depth in zip(['0_5', '5_15', '15_30'],[5, 10, 15]):
        src = rasterio.open(f'{settings.soilgrids_dir}{country_code}_{depth_code}_mean.tif')
        coord_list = [(x,y) for x,y in zip(gdf_bd_pond['geometry'].x , gdf_bd_pond['geometry'].y)]
        if country_code == 'UY':
            gdf_bd_pond[f'bd_{depth_code}_ponderated'] = [(x/100)*depth / total_depth for x in src.sample(coord_list)] # bad bdod values for UY
        else:
            gdf_bd_pond[f'bd_{depth_code}_ponderated'] = [x*depth / total_depth for x in src.sample(coord_list)]

    gdf_bd_pond[f'bd_0_30_ponderated'] = gdf_bd_pond.apply(lambda x: x['bd_0_5_ponderated'] + x['bd_5_15_ponderated'] + x['bd_15_30_ponderated'], axis=1)

    return gdf_bd_pond

def join_with_wosis_data(country_name, gdf_bd_pond):
    profiles = pd.read_csv(f'{settings.output_dir}{country_name}_profile_summary.csv')

    df = profiles[profiles['country_name'] == 'Uruguay'].copy()
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df = df.merge(gdf_bd_pond[['profile_id', 'latitude', 'longitude', 'bd_0_30_ponderated']], on='profile_id')
    df['bd_0_30_soilgrids'] = df['bd_0_30_ponderated'].apply(lambda x: x[0])
    df.drop('bd_0_30_ponderated', axis=1, inplace=True)
    return df


def plot_raster_with_profiles(country_name):
    country_code = country_map[country_name]
    gdf = gpd.read_file(settings.wosis_dir + f"wosis_latest_profiles_{country_name}.shp").to_crs(settings.flat_crs)

    files_re = re.compile(f'{country_code}_[\w]*')
    files = []

    ## scan local directory for shape files
    with os.scandir(settings.soilgrids_dir) as entries:
        for entry in entries:
            if re.search(files_re, entry.name):
                print(entry.name)
                files.append(settings.soilgrids_dir + entry.name)
    files.sort()
    
    bbox = list([c.bbox for c in country_subunits_by_iso_code(country_code)][0]) # returns tuple inside list
    bbox = transform_crs("epsg:4326", settings.flat_crs, bbox)

    bboxes = bbox_split_v(bbox, 2)
    fig_idx = 1

    for file, bbox in zip(files, bboxes):
        src = rasterio.open(file)
        fig, ax = plt.subplots(figsize=(12, 10))

        # transform rasterio plot to real world coords
        extent=[src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
        ax = rasterio.plot.show(src, extent=extent, ax=ax, cmap='pink')
        gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]].plot(ax=ax, markersize=12)
        plt.savefig('{country_name}_raster_with_profiles_{fig_idx}.png')
        fig_idx += 1

def transform_crs(crs_from, crs_to, bbox):
    t = Transformer.from_crs(crs_from=crs_from, crs_to=crs_to, always_xy=True)
    bbox[0], bbox[1] = t.transform(bbox[0], bbox[1])
    bbox[2], bbox[3] = t.transform(bbox[2], bbox[3])
    return bbox

def get_bulk_density(bbox, depth, file_id):
    # get data from SoilGrids
    soil_grids = SoilGrids()
    filename = f'{settings.data_dir}soilgrids/{file_id}_{depth.replace("-","_")}_mean.tif'
    print('destination tif: ', filename)
    if not exists(filename):
        print('getting coverage data with bounding box:', bbox)
        data = soil_grids.get_coverage_data(service_id='bdod', coverage_id=f'bdod_{depth}cm_mean', 
                                            west=bbox[0], south=bbox[1], east=bbox[2], north=bbox[3],                                     
                                            crs='urn:ogc:def:crs:EPSG::3857', local_file=False,
                                            output=filename)
    else: 
        print(f'{filename} already exists')
    return rasterio.open(filename)    

# split the bounding box to a matrix of boxes.
def bbox_split(bbox, splits):
    print('original bbox:', bbox)
    bboxes = []
    west_bound = bbox[0]
    south_bound = bbox[1]
    east_bound = bbox[2]
    north_bound = bbox[3]
    hdif = east_bound - west_bound
    vdif = north_bound - south_bound
    for i in range(splits):
        s = south_bound + i*vdif/splits
        n = s + vdif/splits
        for j in range(splits):   
            w = west_bound + j*hdif/splits
            e = w + hdif/splits
            bboxes.append([w, s, e, n])
    return bboxes

    # split the bounding box vertically.
def bbox_split_v(bbox, splits):
    print('original bbox:', bbox)
    bboxes = []
    south_bound = bbox[1]
    north_bound = bbox[3]
    vdif = north_bound - south_bound
    for i in range(splits):
        s = south_bound + i*vdif/splits
        n = s + vdif/splits
        bboxes.append([bbox[0], s, bbox[2], n])
    return bboxes