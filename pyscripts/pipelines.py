import argparse
import logging
import pandas as pd

from pyscripts.wosis_utils import fetch_wosis_latest_profiles
from pyscripts import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def wosis_report_for_country(country_name):

    if country_name not in settings.countries:
        raise ValueError(f'Please input one of the following countries: {settings.countries}')

    df = fetch_wosis_latest_profiles(country_name)
    df.to_csv(f'{settings.output_dir}{country_name}_profile_summary.csv')
