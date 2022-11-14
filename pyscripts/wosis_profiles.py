# import libraries
import subprocess
import os
import logging
from pathlib import Path

# local files
from pyscripts import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def fetch_wosis_latest_profiles(country_name):
    for prop in settings.properties:
        call_r_script(country_name, 'SHP', prop)

def call_r_script(country_name, type, property):
    filename = f'{settings.data_dir}/{settings.wosis_dir}/wosis_latest_{property}_{country_name}.{type.lower()}'
    my_file = Path(filename)
    if (my_file.is_file() == True):
        logger.warning(f'file {filename} already exists, remove file first if you wish to update')
    else:
        subprocess.call([f"sudo Rscript gdal_wosis.R {country_name} {type} {property}"], shell=True)
        logger.info(f'data downloaded to path: {filename}')

    return filename