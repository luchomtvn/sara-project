from pyscripts.get_wosis_data import call_r_script
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    call_r_script('Argentina', 'CSV', 'clay')