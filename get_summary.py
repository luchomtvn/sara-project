# this is a script that consumes from pyscripts files and is tested in test subdir. 
# it is expected to be executed by a command line and to be passed arguments.

from pyscripts.pipelines import wosis_report_for_country
import argparse

parser = argparse.ArgumentParser(description='get summary info for profiles, ecologic regions and soil zones, given a country name.')
parser.add_argument('country', help='countries to get summary from')

args = parser.parse_args()
country_name = args.country

wosis_report_for_country(country_name)