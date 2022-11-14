import pytest
import unittest
from pyscripts.get_wosis_data import call_r_script
from pyscripts import settings
from pathlib import Path
import warnings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestCommon(unittest.TestCase):
    def test_call_r_script(self):
        file = settings.data_dir + "/wosis_latest/wosis_latest_clay_Argentina.csv"
        my_file = Path(file)
        if (my_file.is_file() == True):
            self.assertTrue(call_r_script('Argentina', 'CSV', 'clay'), file)
        else:
            self.assertTrue(call_r_script('Argentina', 'CSV', 'clay'), file)
        self.assertTrue(my_file.is_file())


if __name__ == '__main__':
    unittest.main()