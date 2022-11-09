import pytest
import unittest
from pyscripts.get_wosis_data import call_r_script
from pathlib import Path
import warnings
 


class TestCommon(unittest.TestCase):
    def test_call_r_script(self):
        file = "wosis_latest/wosis_latest_clay_Argentina.csv"
        my_file = Path(file)
        if (my_file.is_file() == True):
            warnings.warn(UserWarning(f"file {file} already exists"))
            self.assertTrue(True)
        call_r_script('Argentina', 'CSV', 'clay')
        self.assertTrue(my_file.is_file())


if __name__ == '__main__':
    unittest.main()