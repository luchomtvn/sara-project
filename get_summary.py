# this is a script that consumes from pyscripts files and is tested in test subdir. 
# it is expected to be executed by a command line and to be passed arguments.

from pyscripts.pipelines import wosis_report_for_country, soilgrids_complement_bdod, create_summary_with_regions
import pyscripts.settings as settings
import argparse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='get summary info for profiles, ecologic regions and soil zones, given a country name.')
parser.add_argument('country', help='countries to get summary from')

args = parser.parse_args()
country_name = args.country

if country_name not in settings.countries:
    logger.error("invalid country")
    raise ValueError(f'Please input one of the following countries: {settings.countries}')

wosis_report_for_country(country_name)
soilgrids_complement_bdod(country_name)
create_summary_with_regions(country_name)