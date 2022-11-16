import unittest
import pandas as pd
import numpy as np
from pyscripts.wosis_utils import wosis_ogr2ogr, scan_input_directory, get_armonized_dataset, poderate_avg, get_profile_summary
from pyscripts import settings
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestWosisSource(unittest.TestCase):
    def test_wosis_ogr2ogr(self):
        file = settings.data_dir + "wosis_latest/wosis_latest_clay_Argentina.csv"
        logger.info(file)
        my_file = Path(file)
        if (my_file.is_file() == True):
            self.assertTrue(wosis_ogr2ogr('Argentina', 'CSV', 'clay'), file)
        else:
            self.assertTrue(wosis_ogr2ogr('Argentina', 'CSV', 'clay'), file)
        self.assertTrue(my_file.is_file())

    def test_scan_input_directory(self):
        files = scan_input_directory('Uruguay')
        logger.info(f'local wosis files found for Uruguay: {files}')
        self.assertTrue(files)

    def test_poderate_avg(self):
        df = pd.DataFrame(np.array([[63821, 53190, 0, 7, 9.7],
                                    [63821, 53191, 7, 23, 11.9],
                                    [63821, 53192, 23, 45, 14.0],
                                    [63821, 53193, 45, 100, 6.8],
                                    [63822, 53194, 0, 25, 5.0],
                                    [63823, 53195, 0, 17, 2.0],
                                    [63823, 53196, 17, 34, 2.0],
                                    [63823, 53197, 34, 58, 3.0],
                                    [63823, 53198, 58, 100, 4.0]]), columns=['profile_id', 'profile_layer_id', 'upper_depth', 'lower_depth', 'orgc_value_avg'])
        df['orgc_pond_val'] = df.apply(poderate_avg, args=('orgc', 30), axis=1)
        self.assertEqual(df.loc[0, 'orgc_pond_val'], 2.26)

    def test_get_profile_summary(self):
        df = pd.DataFrame(np.array([[63821, 'Argentina', 0, 7, 45],
                                    [63822, 'Argentina', 7, 23, 12],
                                    [63823, 'Argentina', 23, 45, 16],
                                    [63824, 'Argentina', 45, 100, 31],
                                    [63825, 'Argentina', 0, 25, 10]]), columns=['profile_id', 'country_name', 'upper_depth', 'lower_depth', 'clay_value_avg'])
        df_summary = get_profile_summary(df, 'clay')
        self.assertEqual(df_summary.loc[0, 'clay_pond_val'], 10.5)

    def test_get_armonized_dataset(self):
        # TODO: should generate files.
        df = get_armonized_dataset('Uruguay')
        self.assertTrue(df.info)
        self.assertEqual(df.loc[0, 'clay_pond_val'], 115.35)


if __name__ == '__main__':
    unittest.main()
