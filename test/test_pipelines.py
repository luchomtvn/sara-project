import pytest
import unittest
from pyscripts.pipelines import wosis_report_for_country, soilgrids_complement_bdod
from pyscripts import settings
from pathlib import Path
import warnings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestCommon(unittest.TestCase):
    def test_wosis_report_for_country(self):
        wosis_report_for_country('Uruguay')
        file = 'Uruguay_profile_summary.csv'
        self.assertTrue(Path(settings.output_dir + file).is_file())

    def test_soilgrids_complement_bdod(self):
        soilgrids_complement_bdod('Uruguay')
        file = 'Uruguay_profile_summary_with_bdod.csv'
        self.assertTrue(Path(settings.output_dir + file).is_file())

if __name__ == '__main__':
    unittest.main()
