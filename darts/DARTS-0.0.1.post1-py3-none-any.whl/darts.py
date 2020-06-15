import os
import torch
import numpy as np
import pandas as pd
import nibabel
from sys import exit
from DARTS.models.dense_unet_model import Dense_Unet
from DARTS.utils import load_data, back_to_original_4_pred
from DARTS.region_names import region_names_dict

class Segmentation():
    def __init__(self, model_wts_path='./dense_unet_back2front_finetuned.pth'):
        """
        Initializes the segmentation object (GPU required)
        Parameters
        ----------
        model_wts_path : Path to pre-trained model (default './dense_unet_back2front_finetuned.pth')
        """
        super(Segmentation, self).__init__()

        if torch.cuda.is_available():
            self.device = 'cuda'
            self.model = Dense_Unet(in_chan = 1, out_chan = 113, filters = 256, num_conv = 4)
            self.model.load_state_dict(torch.load(model_wts_path))
            self.model = self.model.to(self.device)
            self.model.eval()
            self.input_image = None
        else:
            exit("GPU required")

    def read_image(self, input_image_path):
        """
        Normalizes specified input and output as np.array
        Parameters
        ----------
        input_image_path : Path to input image (can be .mgh, .mgz, .nii or .nii.gz)

        Returns
        -------
        Normalized input MRI as np.array
        """

        if ".mg" in str.lower(input_image_path):
            is_mgz = True
        else:
            is_mgz = False

        input_image, orient, pad_sh1, sh1, pad_sh2, sh2, pad_sh3, sh3, affine_map = load_data(input_image_path, is_mgz)
        input_image[np.isnan(input_image)] = 0
        input_image = np.clip(input_image, a_min=0.0, a_max=np.max(input_image))

        remove_idx_list = [34, 35, 42, 43, 73, 74, 77, 78, 108, 109]
        self.keep_idx_list = [i for i in range(113) if i not in remove_idx_list]

        self.sh2 = input_image.shape[2]
        input_image = torch.from_numpy(input_image).to(self.device).float()
        for i in range(self.sh2):
            max_value = torch.max(input_image[:, :, i])
            min_value = torch.min(input_image[:, :, i])
            input_image[:, :, i] = (input_image[:, :, i] - min_value) / (max_value - min_value + 1e-4)

        self.input_image = input_image
        self.orient, self.pad_sh1, self.sh1, self.pad_sh2, self.sh2, self.pad_sh3, self.sh3, self.affine_map = orient, pad_sh1, sh1, \
                                                                                              pad_sh2, sh2, pad_sh3, sh3, affine_map

        return self.input_image

    def predict(self, input_image_path, output_dir='./'):
        """
        Segments the input image
        Parameters
        ----------
        input_image_path : Path to input image (can be .mgh, .mgz, .nii or .nii.gz)
        output_dir : Path to save segmentation output and volumes (default: './')

        Returns
        -------
        Segmentation mask (np.array)
        """
        _ = self.read_image(input_image_path)
        print("Segmenting image")
        sh2 = self.input_image.shape[2]
        keep_idx_list = self.keep_idx_list
        pred_arg_max = [0] * sh2  # stores the prediction
        for i in range(sh2):
            out = self.model(self.input_image[:, :, i].unsqueeze(0).unsqueeze(1))
            out = out[:, keep_idx_list, :, :]
            pred_arg_max[i] = torch.argmax(out, dim=1).data.cpu().numpy()
        pred_arg_max = np.moveaxis(np.concatenate(pred_arg_max, axis=0), 0, -1)
        pred_orig = back_to_original_4_pred(pred_arg_max, self.orient, self.pad_sh1, self.sh1, self.pad_sh2, \
                                            self.sh2, self.pad_sh3, self.sh3)
        #change labels
        pred_orig[pred_orig == 102] = 103
        pred_orig[pred_orig == 0] = 102
        pred_orig[pred_orig == 103] = 0

        print("Segmentation complete, saving predictions")

        self.save_output_one(pred_orig, input_image_path, output_dir)
        return pred_orig

    def save_output_one(self, pred_orig, input_image_path, output_dir='./'):
        """
        Saves the input image and volumes
        Parameters
        ----------
        pred_orig : Segmentation mask (np.array)
        input_image_path : Path to input image (can be .mgh, .mgz, .nii or .nii.gz)
        output_dir : Path to save segmentation output and volumes (default: './')
        """

        file_name = input_image_path.split('.')[0].split('/')[-1]
        if ".mg" in str.lower(input_image_path):
            pred_orig_nib = nibabel.freesurfer.mghformat.MGHImage(pred_orig.astype(np.float32), None)
            nibabel.save(pred_orig_nib, os.path.join(output_dir, file_name+'_seg.mgz'))
        else:
            pred_orig_nib = nibabel.Nifti1Image(pred_orig, None)
            nibabel.save(pred_orig_nib, os.path.join(output_dir, file_name+'_seg.nii.gz'))

        if ".mg" in str.lower(input_image_path):
            seg = nibabel.freesurfer.MGHImage.from_filename(os.path.join(output_dir,file_name+'_seg.mgz'))
            if np.sum(seg.affine[:,:3] != self.affine_map[:,:3]) != 0:
                pred_orig_nib = nibabel.freesurfer.mghformat.MGHImage(seg.get_data().astype(np.float32), self.affine_map)
                nibabel.save(pred_orig_nib, os.path.join(output_dir, file_name+'_seg.mgz'))
        else:
            seg = nibabel.load(os.path.join(output_dir, file_name+'_seg.nii.gz'))
            if np.sum(seg.affine[:, :3] != self.affine_map[:,:3]) != 0:
                pred_orig_nib = nibabel.Nifti1Image(seg.get_data(), self.affine_map)
                nibabel.save(pred_orig_nib, os.path.join(output_dir, file_name+'_seg.nii.gz'))

        # make volumes dictionary
        unique, counts = np.unique(pred_orig_nib.get_data(), return_counts=True)
        volumes = counts * (pred_orig_nib.header.get_zooms()[0] * pred_orig_nib.header.get_zooms()[1] * pred_orig_nib.header.get_zooms()[2])
        volumes_dict= dict(zip(unique.astype(int), volumes))
        # save to csv
        df = pd.DataFrame.from_dict(volumes_dict, orient = "index", columns=["Volume (voxels)"])
        df.index.name = "Label Number"
        dict_2 = {}
        for i in unique:
            dict_2[i] = region_names_dict[i]
        df.insert(0, "Region", dict_2.values())
        df.to_csv(os.path.join(output_dir, file_name+"_volumes.csv"))

        print("Segmented image and volumes saved at", output_dir)
