import pytest
import unittest
from pyscripts.shp_utils import (
    load_shape_file_into_gdf, csv_to_shp, 
    get_region_and_profile_to_merge, get_bbox_and_transform,
    plot_profile_with_regions
)
from country_bounding_boxes import country_subunits_by_iso_code
from pyscripts import settings
from pathlib import Path
import warnings
import logging
import rasterio
import os
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestLoadingSHPFiles(unittest.TestCase):

    def test_get_bbox_and_transform(self):
        bbox = get_bbox_and_transform('UY')
        self.assertEquals(bbox[0], -6505303.405015289)

    def test_load_shape_file_into_gdf(self):
        gdf = load_shape_file_into_gdf('LAC-SOTER')
        self.assertTrue(gdf.loc[0,'AREA'])

    def test_csv_to_shp(self):
        filepath = os.path.join(settings.output_dir, f'Uruguay_profile_summary_with_bdod.csv')
        df = pd.read_csv(filepath)
        gdf = csv_to_shp(df, 'longitude', 'latitude', transform_crs=True, flat_crs="EPSG:3857")
        gdf.loc[0, 'geometry']
        self.assertTrue(True)

    def test_get_region_and_profile_to_merge(self):
        gdf_regions, gdf_profiles = get_region_and_profile_to_merge('Uruguay', 'remapasdesuelo')        
        gdf_regions.loc[0, 'geometry']    
        gdf_profiles.loc[0, 'geometry']
        self.assertTrue(True)

    def test_plot_profile_with_regions(self):
        plot_profile_with_regions('Uruguay', 'sa_eco_l3', 'LEVEL3', "PERFILES Y ZONAS ECOLOGICAS - URUGUAY")
        self.assertTrue(Path(os.path.join(settings.output_dir, "PERFILES Y ZONAS ECOLOGICAS - URUGUAY.png")).is_file())

if __name__ == '__main__':
    unittest.main()
