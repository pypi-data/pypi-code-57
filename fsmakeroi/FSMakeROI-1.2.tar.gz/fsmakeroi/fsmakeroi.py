"""
A CLI tool to extract ROIs from Freesurfer's segmentation file
"""

#---------------------------------------------------------------------
# Package Management
#---------------------------------------------------------------------
import os
import os.path as op
import numpy as np
import argparse
import textwrap
import fsmakeroi.iocontrol as io
from tqdm import tqdm
import nibabel as nib

def main():
    #-----------------------------------------------------------------
    # Parse Arguments
    #-----------------------------------------------------------------
    parser = argparse.ArgumentParser(
        prog='FSMakeROI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            '''\
                Information
                -----------
                FSMakeROI is a CLI tool that reads in Freesurfer
                segmentation file and extracts ROIs into an output
                directory. If an image is also provided, this tool
                extracts the ROI from it.

                Example
                -------
                
                Running an any aparc+aseg.mgz file with
                example roi.txt will produce 4 ROI files in output
                directory. Use the command:

                fsmakeroi \\
                    /FS_Output/Subject_ID/mri/aparc+aseg.mgz \\
                    examples/example_roi.txt \\
                    -o /Data/Subject_ID/ROI
            '''
        )
    )
    # mandatory arguments
    parser.add_argument(
        'aseg',
        help='Path to aparc+aseg.mgz file',
        type=str
    )
    parser.add_argument(
        'roi',
        help='Path to text file containing ROI codes',
        type=str
    )
    # optional arguments
    parser.add_argument(
        '-i', '--image',
        help='Path to image to apply the ROIs to',
        type=str
    )
    parser.add_argument(
        '-o', '--output',
        help='Output directory to save files',
        type=str
    )
    # parse arguments
    args = parser.parse_args()

    #-----------------------------------------------------------------
    # Validate Arguments
    #-----------------------------------------------------------------
    if not op.exists(args.aseg):
        raise FileNotFoundError('Segmentation file {} not '
        'found'.format(args.aseg))
    if op.splitext(args.aseg)[-1] != '.mgz':
        raise IOError('Segmentatation file does not possess a '
        'valid .mgz extension')
    if not op.exists(args.roi):
        raise FileNotFoundError('ROI code file {} not '
        'found'.format(args.roi))
    if args.image:
        if not op.exists(args.image):
            raise FileNotFoundError('Image file {} not '
            'found'.format(args.image))
    if args.output:
        if not op.isdir(args.output):
            raise NotADirectoryError('Output directory {} not '
            'found'. format(args.output))
    else:
        args.output = os.getcwd()
    
    #-----------------------------------------------------------------
    # Run Program
    #-----------------------------------------------------------------
    working_dir = os.path.abspath(os.path.dirname(__file__))
    lut = io.readlut(
        op.join(working_dir, 'FsTutorial_AnatomicalROI_FreeSurferColorLUT.txt'))
    rois = io.readroi(args.roi)
    aseg = nib.load(args.aseg)
    aseg_img = np.array(aseg.dataobj)
    lut_usr = lut[lut['Label'].isin(rois)]
    nrois = len(lut_usr.index)
    if args.image:
        fn_prefix = op.splitext(op.basename(args.image))[0]
        img = nib.load(args.image).dataobj
    else:
        fn_prefix = ''
        img = np.ones_like(aseg_img, dtype=bool)
    for i in tqdm(range(nrois), unit='roi'):
        if fn_prefix:
            fn = op.join(args.output, fn_prefix + '_' + lut_usr['Name'].iloc[i] + '.nii.gz')
        else:
            fn = op.join(args.output, lut_usr['Name'].iloc[i] + '.nii.gz')
        tqdm.write('Writing {}'. format(fn))
        aseg_roi = (aseg_img == lut_usr['Label'].iloc[i]) * np.array(img)
        img_2_write = nib.Nifti1Image(
            aseg_roi,
            aseg.affine,
            aseg.header
        )
        nib.save(img_2_write, fn)
