import argparse
import logging
import pandas as pd
import os

from pyscripts.wosis_utils import fetch_wosis_latest_profiles
from pyscripts.soilgrids_utils import complement_bdod
from pyscripts import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def wosis_report_for_country(country_name):
    df = fetch_wosis_latest_profiles(country_name)
    if not os.path.exists(settings.output_dir):
        os.mkdir(settings.output_dir)
    df.to_csv(f'{settings.output_dir}{country_name}_profile_summary.csv')


def soilgrids_complement_bdod(country_name):
    df = complement_bdod(country_name, download_rasters=False, plot=False)
    df.to_csv(
        f'{settings.output_dir}{country_name}_profile_summary_with_bdod.csv')
