import pytest
import unittest
from pyscripts.soilgrids_utils import (
    get_bulk_density, transform_crs, get_raster_files,
    ponderate_soilgrids_rasters, join_with_wosis_data,
    complement_bdod
)
from country_bounding_boxes import country_subunits_by_iso_code
from pyscripts import settings
from pathlib import Path
import warnings
import logging
import rasterio

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestSoilgridsSource(unittest.TestCase):
    def test_get_bulk_density(self):
        subunits = country_subunits_by_iso_code('UY')
        bbox = transform_crs(subunits, "epsg:4326", settings.flat_crs)
        file = settings.soilgrids_dir + 'UY_0_5_mean.tif'
        self.assertEqual(rasterio.open(file).name,
                         get_bulk_density(bbox, '0-5', 'UY').name)

    def test_get_raster_files(self):
        get_raster_files('Uruguay')
        self.assertTrue(Path(settings.soilgrids_dir +
                        'UY_0_5_mean.tif').is_file())
        self.assertTrue(Path(settings.soilgrids_dir +
                        'UY_5_15_mean.tif').is_file())
        self.assertTrue(Path(settings.soilgrids_dir +
                        'UY_15_30_mean.tif').is_file())

    def test_ponderate_soilgrids_rasters(self):
        df = ponderate_soilgrids_rasters('Uruguay')
        self.assertEqual(df.loc[0, 'bd_0_30_ponderated'], 1.355)

    def test_join_with_wosis_data(self):
        df_pond = ponderate_soilgrids_rasters('Uruguay')
        df = join_with_wosis_data('Uruguay', df_pond)
        self.assertEqual(df.loc[0, 'bd_0_30_soilgrids'], 1.59)

    def test_complement_bdod(self):
        df = complement_bdod('Uruguay', download_rasters=False, plot=False)
        self.assertEqual(df.loc[0, 'bd_0_30_soilgrids'], 1.59)


if __name__ == '__main__':
    unittest.main()
