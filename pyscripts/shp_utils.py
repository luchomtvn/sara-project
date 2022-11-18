import pandas as pd
import geopandas as gpd
import os
import matplotlib.pyplot as plt
from country_bounding_boxes import country_subunits_by_iso_code
from pyscripts.soilgrids_utils import transform_crs, country_map
import pyscripts.settings as settings

soil_data_map = {
    'Uruguay': 'zonas_suelo_uy'
}

path_map = {
    'LAC-SOTER': "LAC-SOTER/SOTERLAC/GIS/SOTER/SOTERLACv2.shp",
    'sa_eco_l3': "sa_eco_l3/sa_eco_l3.shp",
    'zonas_suelo_uy': "zonas_suelo_uy/geomorfologico_utm.shp",
    'zonas_suelo_ar': "zonas_suelo_ar/suelos_500000_v9.shp",
    'country_borders': "country_borders/paisesCopy_ll-wgs84.shp"
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
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
        df.loc[:, long_col], df.loc[:, lat_col])).set_crs("EPSG:4326")
    gdf.drop('Unnamed: 0', axis=1, inplace=True)
    if transform_crs:
        return gdf.to_crs(flat_crs)
    return gdf

def add_zone_names_to_ecoregions(df_eco):
    with open(settings.data_dir + 'ecozone_names.txt', 'r') as ecozones:
        zones = ecozones.readlines()
    zone_names = list(map(extract_zone_names, zones))
    levels = list(map(extract_levels, zones))
    df_level_zone = pd.DataFrame(list(zip(levels, zone_names)), columns=['level', 'zone_name'])
    return df_eco.merge(df_level_zone, left_on='LEVEL3', right_on='level')

def get_region_and_profile_to_merge(country_name, shape_dir_path):
    summary_path = os.path.join(
        settings.output_dir, f'{country_name}_profile_summary_with_bdod.csv')
    return load_shape_file_into_gdf(shape_dir_path), csv_to_shp(pd.read_csv(summary_path), 'longitude', 'latitude')


def plot_profile_with_regions(country_name, shape_dir_path, column_plot, plot_title, to_file=False):
    shapes_df, profiles_gdf = get_region_and_profile_to_merge(
        country_name, shape_dir_path)

    # region plot
    fig, ax = plt.subplots(1, 1, figsize=(15, 8))
    bbox = get_bbox_and_transform(country_map[country_name])
    base = shapes_df.clip(mask=(bbox[0], bbox[1], bbox[2], bbox[3])).plot(
        column=column_plot, ax=ax)

    # profiles plot
    profiles_gdf.plot(ax=base, marker='o', color='blue', markersize=5)

    # country border plot
    country_borders_gdf = load_shape_file_into_gdf('country_borders')
    country_borders_gdf.boundary.clip(
        mask=(bbox[0], bbox[1], bbox[2], bbox[3])).plot(ax=base, color='black')
    base.set_title(plot_title)
    if to_file:
        plt.savefig(os.path.join(settings.output_dir, plot_title + '.png'))
    else:
        plt.show()

def merge_soil_with_regions_and_create_summary(country_name):
    bbox = get_bbox_and_transform(country_map[country_name])
    gdf_eco_no_names = load_shape_file_into_gdf('sa_eco_l3')
    gdf_eco = add_zone_names_to_ecoregions(gdf_eco_no_names)
    gdf_suelos, profiles_gdf = get_region_and_profile_to_merge(country_name, soil_data_map[country_name])
    gdf_zones = gdf_suelos.overlay(gdf_eco.clip(mask=(bbox[0], bbox[1], bbox[2], bbox[3])))
    profile_zones = gdf_zones.sjoin(profiles_gdf, predicate='contains')

    group_profile_zones = profile_zones[['GEOFORMA', 'zone_name', 'profile_id', 'clay_pond_val', 'orgc_pond_val', 'bdfi33_pond_val', 'bd_0_30_soilgrids']] \
                    .groupby(['GEOFORMA', 'zone_name']).agg({'profile_id':'count',
                                            'clay_pond_val':['mean', 'std'],
                                            'orgc_pond_val':['mean', 'std'],
                                            'bdfi33_pond_val':['mean', 'std'],
                                            'bd_0_30_soilgrids':['mean', 'std']})
    group_profile_zones.to_excel(os.path.join(settings.output_dir, f'profile_zones_{country_name}.xlsx'))

def extract_levels(line):
    levels = line.split(' ')[0]
    if levels[-1] == '.':
        return levels[:-1]
    else:
        return levels

def extract_zone_names(line):
    zone_name = line.split('.')[-1]
    zone_name = zone_name.split(" ", 1)[1]
    return zone_name.strip()