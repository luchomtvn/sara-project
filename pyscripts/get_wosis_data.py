import subprocess
import os
from pyscripts import settings


def call_r_script(country, type, property, update=False):
    if update:
        filename = f'wosis_latest_{property}_{country}.{type.lower()}'
        os.remove(settings.data_dir + settings.wosis_dir + filename)
    subprocess.call([f"sudo Rscript gdal_wosis.R {country} {type} {property}"], shell=True)
