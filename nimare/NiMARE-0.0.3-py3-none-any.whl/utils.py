"""
Utilities
"""
from __future__ import division

import re
import logging
import os.path as op

import numpy as np
import pandas as pd
import nibabel as nib
from nilearn import datasets
from nilearn.input_data import NiftiMasker

LGR = logging.getLogger(__name__)


def get_template(space='mni152_1mm', mask=None):
    """
    Load template file.

    Parameters
    ----------
    space : {'mni152_1mm', 'mni152_2mm', 'ale_2mm'}, optional
        Template to load. Default is 'mni152_1mm'.
    mask : {None, 'brain', 'gm'}, optional
        Whether to return the raw template (None), a brain mask ('brain'), or
        a gray-matter mask ('gm'). Default is None.

    Returns
    -------
    img : :obj:`nibabel.nifti1.Nifti1Image`
        Template image object.
    """
    if space == 'mni152_1mm':
        if mask is None:
            img = nib.load(datasets.fetch_icbm152_2009()['t1'])
        elif mask == 'brain':
            img = nib.load(datasets.fetch_icbm152_2009()['mask'])
        elif mask == 'gm':
            img = datasets.fetch_icbm152_brain_gm_mask(threshold=0.2)
        else:
            raise ValueError('Mask {0} not supported'.format(mask))
    elif space == 'mni152_2mm':
        if mask is None:
            img = datasets.load_mni152_template()
        elif mask == 'brain':
            img = datasets.load_mni152_brain_mask()
        elif mask == 'gm':
            # this approach seems to approximate the 0.2 thresholded
            # GM mask pretty well
            temp_img = datasets.load_mni152_template()
            data = temp_img.get_fdata()
            data = data * -1
            data[data != 0] += np.abs(np.min(data))
            data = (data > 1200).astype(int)
            img = nib.Nifti1Image(data, temp_img.affine)
        else:
            raise ValueError('Mask {0} not supported'.format(mask))
    elif space == 'ale_2mm':
        if mask is None:
            img = datasets.load_mni152_template()
        else:
            # Not the same as the nilearn brain mask, but should correspond to
            # the default "more conservative" MNI152 mask in GingerALE.
            img = nib.load(op.join(get_resource_path(),
                           'templates/MNI152_2x2x2_brainmask.nii.gz'))
    else:
        raise ValueError('Space {0} not supported'.format(space))
    return img


def get_masker(mask):
    """
    Get an initialized, fitted nilearn Masker instance from passed argument.

    Parameters
    ----------
    mask : str, :class:`nibabel.nifti1.Nifti1Image`, or any nilearn Masker

    Returns
    -------
    masker : an initialized, fitted instance of a subclass of
        `nilearn.input_data.base_masker.BaseMasker`
    """
    if isinstance(mask, str):
        mask = nib.load(mask)

    if isinstance(mask, nib.nifti1.Nifti1Image):
        mask = NiftiMasker(mask)

    if not (hasattr(mask, 'transform') and
            hasattr(mask, 'inverse_transform')):
        raise ValueError("mask argument must be a string, a nibabel image,"
                         " or a Nilearn Masker instance.")

    # Fit the masker if needed
    if not hasattr(mask, 'mask_img_'):
        mask.fit()

    return mask


def listify(obj):
    """
    Wraps all non-list or tuple objects in a list; provides a simple way
    to accept flexible arguments.
    """
    return obj if isinstance(obj, (list, tuple, type(None), np.ndarray)) else [obj]


def round2(ndarray):
    """
    Numpy rounds X.5 values to nearest even integer. We want to round to the
    nearest integer away from zero.
    """
    onedarray = ndarray.flatten()
    signs = np.sign(onedarray)  # pylint: disable=no-member
    idx = np.where(np.abs(onedarray - np.round(onedarray)) == 0.5)[0]
    x = np.abs(onedarray)
    y = np.round(x)
    y[idx] = np.ceil(x[idx])
    y *= signs
    rounded = y.reshape(ndarray.shape)
    return rounded.astype(int)


def get_resource_path():
    """
    Returns the path to general resources, terminated with separator. Resources
    are kept outside package folder in "datasets".
    Based on function by Yaroslav Halchenko used in Neurosynth Python package.
    """
    return op.abspath(op.join(op.dirname(__file__), 'resources') + op.sep)


def try_prepend(value, prefix):
    if isinstance(value, str):
        return op.join(prefix, value)
    else:
        return value


def find_stem(arr):
    """
    From https://www.geeksforgeeks.org/longest-common-substring-array-strings/
    """
    # Determine size of the array
    n = len(arr)

    # Take first word from array
    # as reference
    s = arr[0]
    ll = len(s)

    res = ""
    for i in range(ll):
        for j in range(i + 1, ll + 1):
            # generating all possible substrings of our ref string arr[0] i.e s
            stem = s[i:j]
            k = 1
            for k in range(1, n):
                # Check if the generated stem is common to to all words
                if stem not in arr[k]:
                    break

            # If current substring is present in all strings and its length is
            # greater than current result
            if (k + 1 == n and len(res) < len(stem)):
                res = stem

    return res


def uk_to_us(text):
    """
    Convert UK spellings to US based on a converter.

    english_spellings.csv: From http://www.tysto.com/uk-us-spelling-list.html

    Parameters
    ----------
    text : :obj:`str`

    Returns
    -------
    text : :obj:`str`
    """
    SPELL_DF = pd.read_csv(op.join(get_resource_path(), 'english_spellings.csv'),
                           index_col='UK')
    SPELL_DICT = SPELL_DF['US'].to_dict()

    if isinstance(text, str):
        # Convert British to American English
        pattern = re.compile(r'\b(' + '|'.join(SPELL_DICT.keys()) + r')\b')
        text = pattern.sub(lambda x: SPELL_DICT[x.group()], text)
    return text
