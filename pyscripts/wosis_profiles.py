# import libraries
import subprocess
import os
import re
import logging
from pathlib import Path
import pandas as pd

# local files
from pyscripts import settings
import pyscripts.wosis_utils as utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

'''
    get all profile information for a country and apply ponderation to property columns
'''
def fetch_wosis_latest_profiles(country_name):
    for prop in settings.properties:
        wosis_ogr2ogr(country_name, 'SHP', prop)
    return get_armonized_dataset(country_name)

'''
    call r script to fetch wosis latest for a country. Specify property and file type
'''
def wosis_ogr2ogr(country_name, type, property):
    filename = f'{settings.data_dir}/{settings.wosis_dir}/wosis_latest_{property}_{country_name}.{type.lower()}'
    my_file = Path(filename)
    if (my_file.is_file() == True):
        logger.warning(
            f'file {filename} already exists, remove file first if you wish to update')
    else:
        subprocess.call(
            [f"sudo Rscript gdal_wosis.R {country_name} {type} {property}"], shell=True)
        logger.info(f'data downloaded to path: {filename}')

    return filename

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
    for every file found for a country, ponderate and group into a single detaset. 
'''
def get_armonized_dataset(country_name):
    files = scan_input_directory(country_name)
    summarized_profiles = []
    for file in files:
        if(format == 'csv'):
            df = pd.read_csv(settings.wosis_dir + file)
            property = file.split("_")[-2]
            summarized_profiles.append(utils.get_profile_summary(df, property))
    return summarized_profiles

