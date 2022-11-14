from pyscripts.get_wosis_data import call_r_script
from pyscripts import settings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    for country in settings.countries:
        for prop in settings.properties:
            print(f'fetching {prop} data for {country}')
            file = call_r_script(country, settings.type, prop)
            print(f'r_script output: {file}')
