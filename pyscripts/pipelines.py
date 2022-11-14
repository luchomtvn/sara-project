import argparse
import logging

from pyscripts.wosis_profiles import fetch_wosis_latest_profiles
from pyscripts import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_report_for_country(country_name):

    if country_name not in settings.countries:
        raise ValueError(f'Please input one of the following countries: {settings.countries}')

    fetch_wosis_latest_profiles('Uruguay')