# Copyright (c) 2020,Vienna University of Technology,
# Department of Geodesy and Geoinformation
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY, DEPARTMENT OF
# GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""
Tests for the ColorMap().
"""
import os
import shutil
import unittest
import random
import matplotlib.pyplot as plt
import colorcet as cc
from colorella.colormap import ColorMap
import matplotlib.colors as col
import warnings

try:
    from osgeo import gdal
    GDAL_INSTALLED = True
except:
    GDAL_INSTALLED = False


class TestColormap(unittest.TestCase):

    def setUp(self):
        """ Create random test data and set up path """
        self.data_path = os.path.join(os.path.dirname(__file__), "test_data")
        self.output_path = os.path.join(os.path.dirname(__file__), "test_output")
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        cm_mpl_list = plt.colormaps()
        self.default_mpl_cm = random.choice(cm_mpl_list)

        cm_cc_dict = cc.cm
        self.default_cc_cm = random.choice(list(cm_cc_dict.keys()))

        red = [(0., 1, 1), (1, 0, 0)]
        green = [(0., 1, 1), (1, 0, 0)]
        blue = [(0., 1, 1), (1, 0, 0)]
        alpha = [(0., 1, 1), (1, 0, 0)]
        for i in range(4):
            red.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
            green.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
            blue.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
            alpha.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
        red.sort(key=lambda x: x[0])
        green.sort(key=lambda x: x[0])
        blue.sort(key=lambda x: x[0])
        alpha.sort(key=lambda x: x[0])
        self.cdict = {'red': tuple(red), 'green': tuple(green), 'blue': tuple(blue), 'alpha': tuple(alpha)}

        self.clist = []
        for i in range(random.randint(1, 20)):
            self.clist.append((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))

    def tearDown(self):
        """ Removes all test data """
        shutil.rmtree(self.output_path)

    def test_ml_cmap_from_name(self):
        """
        Tests creation of a ColorMap from mpl name
        """
        cmap = ColorMap('mpl:{}'.format(self.default_mpl_cm))
        self.assertIsInstance(cmap, ColorMap)

    def test_cc_cmap_from_name(self):
        """
        Tests creation of a ColorMap from a cc name
        """
        cmap = ColorMap('cc:{}'.format(self.default_cc_cm))
        self.assertIsInstance(cmap, ColorMap)

    def test_cl_cmap_from_name(self):
        """
        Tests creation of a ColorMap from user colormap directory
        """
        cmap = ColorMap('cl:{}'.format('Rainbow'))
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_dict(self):
        """
        Tests creation of a ColorMap from a dictionary
        """
        cmap = ColorMap.from_dict(self.cdict)
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_list(self):
        """
        Tests creation of a ColorMap from a list
        """
        cmap = ColorMap.from_list(self.clist)
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_ctfile(self):
        """
        Tests creation of a ColorMap from a gdal ct file
        """
        ct_file = 'sgrt_ct_cont_ssm.ct'
        cmap = ColorMap.from_ctfile(os.path.join(self.data_path, ct_file), gradient=False)
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_cpt(self):
        """
        Tests creation of a ColorMap from a matplotlib ColorMap file
        """
        cpt_file = 'ETOPO1.cpt'
        cmap = ColorMap.from_cptfile(os.path.join(self.data_path, cpt_file), gradient=True)
        self.assertIsInstance(cmap, ColorMap)

    def test_cmap_from_json(self):
        """
        Tests creation of a ColorMap from a json file
        """
        json_file = 'Rainbow.json'
        cmap = ColorMap.from_jsonfile(os.path.join(self.data_path, json_file))
        self.assertIsInstance(cmap, ColorMap)

    def test_listed2segmented(self):
        """
        Tests conversion from a Listed ColorMap to a LinearSegmented ColorMap
        """
        cmap = ColorMap.from_list(self.clist)
        cmap = cmap.to_gradient()
        self.assertIsInstance(cmap._mpl_cm, col.LinearSegmentedColormap)

    def test_save_as_cpt(self):
        """
        Tests save ColorMap as cpt file
        """
        cmap = ColorMap('mpl:{}'.format(self.default_mpl_cm))
        cmap.show()
        output_path = os.path.join(self.output_path, 'cpt_test.cpt')
        cmap.save_as_cpt(output_path)
        if isinstance(cmap._mpl_cm, col.LinearSegmentedColormap):
            cmap_read = ColorMap.from_file(output_path, gradient=True)
        if isinstance(cmap._mpl_cm, col.ListedColormap):
            cmap_read = ColorMap.from_file(output_path, gradient=False)
        cmap_read.show()
        self.assertIsInstance(cmap_read, ColorMap)

    def test_save_as_ct(self):
        """
        Tests save ColorMap as ct file
        """
        cmap = ColorMap('mpl:{}'.format(self.default_mpl_cm))
        cmap.show()
        output_path = os.path.join(self.output_path, 'ct_test.ct')
        cmap.save_as_ct(output_path)
        if isinstance(cmap._mpl_cm, col.LinearSegmentedColormap):
            cmap_read = ColorMap.from_file(output_path, gradient=True)
        if isinstance(cmap._mpl_cm, col.ListedColormap):
            cmap_read = ColorMap.from_file(output_path, gradient=False)
        cmap_read.show()
        self.assertIsInstance(cmap_read, ColorMap)

    def test_save_as_json(self):
        """
        Tests save ColorMap as json file
        """
        cmap = ColorMap('mpl:{}'.format(self.default_mpl_cm))
        cmap.show()
        output_path = os.path.join(self.output_path, 'json_test.json')
        cmap.save_as_json(output_path)
        cmap_read = ColorMap.from_jsonfile(output_path)
        cmap_read.show()
        self.assertIsInstance(cmap_read, ColorMap)

    def test_convert2greyscale(self):
        """
        Tests conversion to a greyscale ColorMap
        """
        cmap = ColorMap('mpl:{}'.format(self.default_mpl_cm))
        cmap_grey = cmap.convert2greyscale()
        cmap_grey.show()
        self.assertIsInstance(cmap_grey._mpl_cm, col.LinearSegmentedColormap)

    def test_to_matplotlib(self):
        """
        Tests creation of a matplotlib ColorMap object
        """
        cmap = ColorMap.from_list(self.clist)
        cmap = cmap.to_matplotlib()
        self.assertIsInstance(cmap, col.ListedColormap)

    def test_to_dict(self):
        """
        Tests writing ColorMap colors to dictionary
        """
        cmap = ColorMap.from_dict(self.cdict)
        cdict_out = cmap.to_dict()
        self.assertEqual(self.cdict, cdict_out)

    def test_to_list(self):
        """
        Tests writing ColorMap colors to list
        """
        cmap = ColorMap.from_list(self.clist)
        clist_out = cmap.to_list()
        self.assertListEqual(self.clist, clist_out)

    def test_reverse(self):
        """
        Tests reversing ColorMap colors

        """
        cmap = ColorMap.from_list(self.clist)
        cmap_reverse = cmap.reverse(inplace=False)
        cmap = cmap_reverse.reverse(inplace=False)
        self.assertEqual(cmap._mpl_cm.colors, self.clist)

    def test_view(self):
        """
        Tests ploting the ColorMap
        """
        cmap = ColorMap('mpl:{}'.format(self.default_mpl_cm))
        cmap.show()

    def test_to_gdal(self):
        """
        Tests converting the matplotlib ColorMap to a gdal color table
        """
        if GDAL_INSTALLED:
            cmap = ColorMap('mpl:{}'.format(self.default_mpl_cm))
            g_ct = cmap.to_gdal()
            self.assertIsInstance(g_ct, gdal.ColorTable)


if __name__ == '__main__':
    unittest.main()
