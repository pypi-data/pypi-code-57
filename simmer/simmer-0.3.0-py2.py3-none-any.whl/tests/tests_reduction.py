"""
    isort:skip_file
"""

import os
import sys
import unittest
import urllib.request
import zipfile

# sys.path.append(os.getcwd()[:-6])
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
#
# parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

import astropy.io.fits as pyfits
import simmer.darks as darks
import simmer.drivers as drivers
import simmer.flats as flats
import simmer.image as image
import simmer.insts as i
import numpy as np
import pandas as pd
import simmer.sky as sky


def download_folder(folder, path=None):
    """
    Downloads a .zip file from this projects S3 testing bucket, unzips it,
    and deletes the .zip file.

    Inputs:
        folder : (string) name of the folder to be downloaded.
    """

    folder_dict = {
        "sky_test": "hhs5w81dvok5wp8",
        "dark_test": "ao1ug1kvlr5l4y3",
        "flat_test": "r0gntctnfrjh5zd",
        "PHARO_config_driver": "p3wv7l800fdqx5q",
        "image_test": "9qwa6ojfsk1l5pq",
        "PHARO_image_driver": "p9uivslz7hoym5c",
        "PHARO_integration": "v8l50zm7jbrccqj",
        "shane_quickstart": "q6m6ls2x2186u3p",
    }

    def retrieve_extract(path):
        with zipfile.ZipFile(folder + ".zip", "r") as zip_ref:
            zip_ref.extractall(path)

    url = f"https://www.dropbox.com/s/{folder_dict[folder]}/{folder}.zip?dl=1"
    u = urllib.request.urlopen(url)
    data = u.read()
    u.close()

    with open(f"{folder}.zip", "wb") as f:
        f.write(data)
    if path:
        retrieve_extract(path)
    elif "src" in os.listdir():  # if we're actually running tests
        retrieve_extract("src/simmer/tests/")
    else:  # we're running this in an arbitrary directory
        retrieve_extract("")
    os.remove(folder + ".zip")


def delete_folder(folder):
    if os.listdir(folder):
        for f in os.listdir(folder):
            if folder[-1] == "/":
                path = folder + f
            else:
                path = folder + "/" + f
            if os.path.isfile(path):
                os.remove(path)
            else:  # if it's a directory!
                delete_folder(path)
    os.rmdir(folder)


class DataDownloadException(Exception):
    """Base class for data download exceptions in this module."""

    pass


class TestCreation(unittest.TestCase):

    inst = i.ShARCS()

    def test_create_darks(self):
        print("Testing darks")

        try:
            download_folder("dark_test")
        except:
            raise DataDownloadException(
                "Could not download test data for darks."
            )

        raw_dir, reddir = (
            "src/simmer/tests/dark_test/",
            "src/simmer/tests/dark_test/",
        )
        compare_dark = pyfits.getdata(raw_dir + "compare_dark.fits", 0)
        zero = np.zeros(np.shape(compare_dark))  # only testing flats
        darklist = range(1357, 1360)
        try:
            result = darks.create_darks(raw_dir, reddir, darklist, self.inst)
            delete_folder(raw_dir)
            self.assertCountEqual(
                np.ravel(result - compare_dark), np.ravel(zero)
            )
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_create_flats(self):
        print("Testing flats")

        try:
            download_folder("flat_test")
        except:
            raise DataDownloadException(
                "Could not download test data for flats."
            )

        raw_dir, reddir = (
            "src/simmer/tests/flat_test/",
            "src/simmer/tests/flat_test/",
        )
        compare_flat = pyfits.getdata(raw_dir + "compare_flat.fits", 0)
        zero = np.zeros(np.shape(compare_flat))  # only testing flats
        flatlist = range(1108, 1114)
        try:
            result = flats.create_flats(
                raw_dir, reddir, flatlist, np.nan, self.inst, test=True
            )

            delete_folder(raw_dir)
            self.assertCountEqual(
                np.ravel(result - compare_flat), np.ravel(zero)
            )
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_create_skies(self):
        print("Testing skies")
        try:
            download_folder("sky_test")
        except:
            raise DataDownloadException(
                "Could not download test data for skies."
            )
        raw_dir, reddir = (
            "src/simmer/tests/sky_test/",
            "src/simmer/tests/sky_test/",
        )
        compare_sky = np.loadtxt(raw_dir + "compare_sky.txt")
        s_dir = raw_dir
        skylist = range(1218, 1222)
        try:
            result = sky.create_skies(
                raw_dir, reddir, s_dir, skylist, self.inst
            )
            zero = np.zeros(np.shape(compare_sky))

            delete_folder(raw_dir)
            self.assertCountEqual(
                np.ravel(result - compare_sky), np.ravel(zero)
            )
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_create_imstack(self):
        print("Testing imstack")

        try:
            download_folder("sky_test")
        except:
            raise DataDownloadException(
                "Could not download test data for skies."
            )
        raw_dir, reddir = (
            "src/simmer/tests/sky_test/",
            "src/simmer/tests/sky_test/",
        )
        imlist = range(1218, 1222)
        s_dir = raw_dir
        try:
            result, shifts_all = image.create_imstack(
                raw_dir, reddir, s_dir, imlist, self.inst
            )
            compare_list = [
                "compare_create_imstack_0",
                "compare_create_imstack_1",
                "compare_create_imstack_2",
                "compare_create_imstack_3",
            ]
            compare_imstack = np.array(
                [np.loadtxt(raw_dir + file) for file in compare_list]
            )
            zero = np.zeros(np.shape(compare_imstack))
            delete_folder(raw_dir)
            self.assertCountEqual(
                np.ravel(result - compare_imstack), np.ravel(zero)
            )
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_create_im_default(self):
        print("Testing default image creation")

        try:
            download_folder("sky_test")
        except:
            raise DataDownloadException(
                "Could not download test data for skies."
            )

        raw_dir, reddir = (
            "src/simmer/tests/sky_test/",
            "src/simmer/tests/sky_test/",
        )
        s_dir = raw_dir
        compare_final_im = pyfits.getdata(
            raw_dir + "Ks/compare_final_im_default.fits", 0
        )
        try:
            image.create_im(s_dir, 10, method="default")
            final_im = pyfits.getdata(raw_dir + "Ks/final_im.fits", 0)
            zero = np.zeros(np.shape(final_im))
            val = np.all(
                np.ravel(final_im - compare_final_im) == np.ravel(zero)
            )
            delete_folder(raw_dir)
            self.assertTrue(val)
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_create_im_saturated(self):
        print("Testing saturated image creation")

        try:
            download_folder("sky_test")
        except:
            raise DataDownloadException(
                "Could not download test data for skies."
            )

        raw_dir, reddir = (
            "src/simmer/tests/sky_test/",
            "src/simmer/tests/sky_test/",
        )
        s_dir = raw_dir
        compare_final_im = pyfits.getdata(
            raw_dir + "Ks/compare_final_im.fits", 0
        )
        try:
            image.create_im(s_dir, 10, method="saturated")
            final_im = pyfits.getdata(raw_dir + "Ks/final_im.fits", 0)
            zero = np.zeros(np.shape(final_im))
            val = np.all(np.allclose(final_im, compare_final_im))
            delete_folder(raw_dir)
            self.assertTrue(val)
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(val)


class TestDrivers(unittest.TestCase):
    inst = i.ShARCS()

    def test_dark_driver(self):
        print("Testing dark driver")

        try:
            download_folder("dark_test")
        except:
            raise DataDownloadException(
                "Could not download test data for darks."
            )

        raw_dir, reddir = (
            "src/simmer/tests/dark_test/",
            "src/simmer/tests/dark_test/",
        )
        config = pd.read_csv(os.getcwd() + "/src/simmer/tests/test_config.csv")
        try:
            darks.dark_driver(raw_dir, reddir, config, self.inst)
            val = "dark_3sec.fits" in os.listdir(raw_dir)
            delete_folder(raw_dir)
            self.assertTrue(val)
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_flat_driver(self):
        print("Testing flat driver")

        try:
            download_folder("flat_test")
        except:
            raise DataDownloadException(
                "Could not download test data for flats."
            )
        raw_dir, reddir = (
            "src/simmer/tests/flat_test/",
            "src/simmer/tests/flat_test/",
        )
        config = pd.read_csv(os.getcwd() + "/src/simmer/tests/test_config.csv")
        source = raw_dir + "flat_J.fits"
        dest = raw_dir + "temp.fits"
        os.rename(source, dest)
        try:
            flats.flat_driver(raw_dir, reddir, config, self.inst)
            val = "flat_J.fits" in os.listdir(raw_dir)
            os.remove(raw_dir + "flat_J.fits")
            os.rename(dest, source)
            delete_folder(raw_dir)
            self.assertTrue(val)
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_sky_driver(self):
        print("Testing sky driver")

        try:
            download_folder("sky_test")
        except:
            raise DataDownloadException(
                "Could not download test data for skies."
            )

        raw_dir, reddir = (
            "src/simmer/tests/sky_test/",
            "src/simmer/tests/sky_test/",
        )
        config = pd.read_csv(os.getcwd() + "/src/simmer/tests/test_config.csv")
        try:
            sky.sky_driver(raw_dir, reddir, config, self.inst)
            val = "sky.fits" in os.listdir(raw_dir + "/K09203794/Ks")
            delete_folder(raw_dir)
            self.assertTrue(val)
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_image_driver(self):
        print("Testing image driver")

        try:
            download_folder("image_test")
        except:
            raise DataDownloadException(
                "Could not download test data for images."
            )

        raw_dir, reddir = (
            "src/simmer/tests/image_test/",
            "src/simmer/tests/image_test/",
        )
        config = pd.read_csv(os.getcwd() + "/src/simmer/tests/test_config.csv")
        try:
            method = image.image_driver(raw_dir, reddir, config, self.inst)
            remove_files = [
                "sh00.fits",
                "sh01.fits",
                "sh02.fits",
                "sh03.fits",
                "shifts.txt",
            ]
            val = np.all(
                [
                    r in os.listdir(raw_dir + f"K09203794/Ks")
                    for r in remove_files
                ]
            )
            delete_folder(raw_dir)
            self.assertTrue(val)
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)


class TestIntegration(unittest.TestCase):
    p = i.PHARO()

    def test_PHARO_all_drivers(self):
        print("Testing PHARO integration")  # need better way to get config?

        try:
            download_folder("PHARO_integration")
        except:
            raise DataDownloadException(
                "Could not download test data for PHARO integration."
            )

        raw_dir, reddir = (
            os.getcwd() + "/src/simmer/tests/PHARO_integration/",
            os.getcwd() + "/src/simmer/tests/PHARO_integration/",
        )
        config_file = os.getcwd() + "/src/simmer/tests/test_image_config.csv"
        try:
            drivers.all_driver(self.p, config_file, raw_dir, reddir)
            compare_final_im = pyfits.getdata(
                raw_dir + "compare_final_im.fits", 0
            )
            final_im = pyfits.getdata(
                raw_dir + "HIP49081/Br-gamma/final_im.fits", 0
            )
            zero = np.zeros(np.shape(final_im))
            val = np.all(
                np.allclose(final_im, compare_final_im, equal_nan=True)
            )

            delete_folder(raw_dir)
            self.assertTrue(val)
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_PHARO_config_drivers(self):
        print(
            "Testing PHARO config integration"
        )  # need better way to get config?

        try:
            download_folder("PHARO_config_driver")
        except:
            raise DataDownloadException(
                "Could not download test data for PHARO config integration."
            )
        raw_dir, reddir = (
            os.getcwd() + "/src/simmer/tests/PHARO_config_driver/",
            os.getcwd() + "/src/simmer/tests/PHARO_config_driver/",
        )
        config_file = os.getcwd() + "/src/simmer/tests/test_image_config.csv"
        try:
            drivers.config_driver(self.p, config_file, raw_dir, reddir)
            sky = pyfits.getdata(raw_dir + "HIP49081/Br-gamma/sky.fits", 0)
            compare_sky = pyfits.getdata(
                raw_dir + "HIP49081/Br-gamma/compare_sky.fits", 0
            )
            zero = np.zeros(np.shape(compare_sky))
            val = np.all(np.allclose(compare_sky, sky, equal_nan=True))

            delete_folder(raw_dir)
            self.assertTrue(val)
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)

    def test_PHARO_image_drivers(self):
        print(
            "Testing PHARO image integration"
        )  # need to actually point to correct folder, change aodirs

        try:
            download_folder("PHARO_image_driver")
        except:
            raise DataDownloadException(
                "Could not download test data for PHARO image driver."
            )
        raw_dir, reddir = (
            os.getcwd() + "/src/simmer/tests/PHARO_image_driver/",
            os.getcwd() + "/src/simmer/tests/PHARO_image_driver/",
        )
        config_file = os.getcwd() + "/src/simmer/tests/test_image_config.csv"
        try:
            drivers.image_driver(self.p, config_file, raw_dir, reddir)
            remove_files = [
                "sh00.fits",
                "sh01.fits",
                "sh02.fits",
                "sh03.fits",
                "shifts.txt",
            ]
            val = np.all(
                [
                    r in os.listdir(raw_dir + "HIP49081/Br-gamma/")
                    for r in remove_files
                ]
            )

            file_dir = os.getcwd() + "/src/simmer/tests/PHARO_image_driver/"
            delete_folder(raw_dir)
            self.assertTrue(val)
        except:
            e = sys.exc_info()[0]
            print(e)
            delete_folder(raw_dir)
            self.assertTrue(False)
