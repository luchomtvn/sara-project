# import libraries
import subprocess
import os
import re
import logging
from pathlib import Path
import pandas as pd
from functools import reduce

# local files
from pyscripts import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

'''
    get all profile information for a country and apply ponderation to property columns
'''


def fetch_wosis_latest_profiles(country_name):
    for prop in settings.properties:
        wosis_ogr2ogr(country_name, 'CSV', prop)
    return get_armonized_dataset(country_name)


'''
    call r script to fetch wosis latest for a country. Specify property and file type
'''


def wosis_ogr2ogr(country_name, type, property):
    filename = f'{settings.wosis_dir}wosis_latest_{property}_{country_name}.{type.lower()}'
    my_file = Path(filename)
    logger.info(filename)
    if (my_file.is_file() == True):
        logger.warning(
            f'file {filename} already exists, remove file first if you wish to update')
    else:
        subprocess.call(
            [f"sudo Rscript {settings.Rscript_path} {country_name} {type} {property}"], shell=True)
        logger.info(f'data downloaded to path: {filename}')

    return filename


'''
    for every file found for a country, ponderate and group into a single detaset. 
'''


def get_armonized_dataset(country_name):
    files = scan_input_directory(country_name)
    logger.info(f'found files for {country_name}: {files}')
    summarized_profiles = []
    for file in files:
        df = pd.read_csv(settings.wosis_dir + file)
        property = file.split("_")[-2]
        summarized_profiles.append(get_profile_summary(df, property))
    return reduce(lambda l, r: pd.merge(l, r, on=['profile_id', 'country_name'], how='outer'), summarized_profiles)


'''
search for downloaded wosis_latest profile information
'''


def scan_input_directory(country_name):
    format = 'csv'  # format is fixed
    country_name = country_name
    properties = '|'.join(settings.properties)

    files_re = re.compile(
        f'wosis_latest_({properties})_({country_name}).{format}')
    files = []
    with os.scandir(settings.wosis_dir) as entries:
        for entry in entries:
            if re.search(files_re, entry.name):
                print(entry.name)
                files.append(entry.name)
    if len(files) == 0:
        logger.warning(f'no wosis latest files found for {country_name}')
    return files


'''
calculate a ponderate value for a property given a limit depth. Works for a pandas dataframe row
'''


def poderate_avg(profiles, property, limit):
    value = float(profiles[property + '_value_avg'])
    upper = float(profiles['upper_depth'])
    lower = float(profiles['lower_depth'])
    if (upper > limit):
        return 0.0

    if (lower > limit):
        partial_depth = limit - upper
        return round((partial_depth * value)/limit, 2)
    else:
        return round(((lower - upper) * value)/limit, 2)


'''
groups a wosis profile dataframe by profile_id and saves summarized information for the calculated ponderates on new column. 
'''


def get_profile_summary(df, property):
    if property == 'profiles':
        return df[['profile_id', 'country_name']]
    else:
        prop_pond_col = property + '_pond_val'
        df[prop_pond_col] = df.apply(poderate_avg, args=(property, 30), axis=1)
        return df[['profile_id', 'country_name', prop_pond_col]].groupby(['profile_id', 'country_name']).sum().reset_index()
