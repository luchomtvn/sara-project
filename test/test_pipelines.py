import pytest
import unittest
from pyscripts.pipelines import wosis_report_for_country
from pyscripts import settings
from pathlib import Path
import warnings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestCommon(unittest.TestCase):
    def test_wosis_report_for_country(self):
        wosis_report_for_country('Uruguay')
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
