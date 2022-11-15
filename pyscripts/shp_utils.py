
from country_bounding_boxes import country_subunits_by_iso_code
from pyscripts.soilgrids_utils import transform_crs, country_map
import pyscripts.settings as settings
import pandas as pd
import geopandas as gpd
import os
import matplotlib.pyplot as plt

path_map = {
    'LAC-SOTER': "LAC-SOTER/SOTERLAC/GIS/SOTER/SOTERLACv2.shp",
    'sa_eco_l3': "sa_eco_l3/sa_eco_l3.shp",
    'remapasdesuelo': "remapasdesuelo/paisesCopy_ll-wgs84.shp"
}

def get_bbox_and_transform(country_code, flat_crs="EPSG:3857"):
    subunits = country_subunits_by_iso_code(country_code)
    return transform_crs(subunits, "epsg:4326", flat_crs)

def get_profiles_and_transform(country_name, flat_crs="EPSG:3857"):
    file = f"{settings.wosis_dir}wosis_latest_profiles_{country_name}.shp"
    gdf = gpd.read_file(file).to_crs(flat_crs)
    return gdf

def load_shape_file_into_gdf(shape_dir_path, transform_crs=True, flat_crs="EPSG:3857"):
    file_path = os.path.join(settings.data_dir, path_map[shape_dir_path])
    gdf = gpd.read_file(file_path)
    if transform_crs:
        return gdf.to_crs(flat_crs)
    
    return gdf

def csv_to_shp(df, long_col, lat_col, transform_crs=True, flat_crs="EPSG:3857"):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.loc[:, long_col], df.loc[:, lat_col])).set_crs("EPSG:4326")
    if transform_crs:
        return gdf.to_crs(flat_crs)
    return gdf


def get_region_and_profile_to_merge(country_name, shape_dir_path):
    summary_path = os.path.join(settings.output_dir, f'{country_name}_profile_summary_with_bdod.csv')
    return load_shape_file_into_gdf(shape_dir_path), csv_to_shp(pd.read_csv(summary_path), 'longitude', 'latitude')

def plot_profile_with_regions(country_name, shape_dir_path, column_plot, plot_title):
    shapes_df, profiles_gdf = get_region_and_profile_to_merge(country_name, shape_dir_path)

    # region plot
    fig, ax = plt.subplots(1, 1, figsize=(15,8))
    bbox = get_bbox_and_transform(country_map[country_name])
    base = shapes_df.clip(mask=(bbox[0], bbox[1], bbox[2], bbox[3])).plot(column=column_plot, ax = ax)

    # profiles plot
    profiles_gdf.plot(ax=base, marker='o', color='blue', markersize=5)

    # country border plot
    country_borders_gdf = load_shape_file_into_gdf('remapasdesuelo')
    country_borders_gdf.boundary.clip(mask=(bbox[0], bbox[1], bbox[2], bbox[3])).plot(ax = base, color='black')
    base.set_title(plot_title)
    plt.savefig(os.path.join(settings.output_dir, plot_title + '.png'))

    
    
