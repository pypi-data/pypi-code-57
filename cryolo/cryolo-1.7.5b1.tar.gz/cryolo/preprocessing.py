#
# COPYRIGHT
# All contributions by Thorsten Wagner:
# Copyright (c) 2017 - 2019, Thorsten Wagner.
# All rights reserved.
#
# ---------------------------------------------------------------------------
#         Do not reproduce or redistribute, in whole or in part.
#      Use of this code is permitted only under licence from Max Planck Society.
#            Contact us at thorsten.wagner@mpi-dortmund.mpg.de
# ---------------------------------------------------------------------------
#

from __future__ import print_function

import difflib
import os

import numpy as np

import cryolo.CoordsIO as CoordsIO
import cryolo.imagereader as imagereader

def get_image_size_distr(img_paths):
    sizes = []
    for timg in img_paths:
        size = imagereader.read_width_height(timg)
        if len(sizes) == 0:
            new = True
        else:
            new = True
            for known_size in sizes:
                if known_size[0] == size[0] and known_size[1] == size[1]:
                    known_size[2] = known_size[2] + 1
                    new = False
                    break
        if new:
            sizes.append([int(size[0]), int(size[1]), 1])
    sizes.sort(key=lambda x: x[2], reverse=True)
    return sizes

def find_image_annotation_pairs(annotations,images):
    img_names = list(map(os.path.basename, images))
    img_annot_pairs = []
    for ann in annotations:
        ann_without_ext = os.path.splitext(os.path.basename(ann))[0]
        cand_list = [i for i in img_names if ann_without_ext in i]
        try:
            cand_list_no_fileextension = list(map(os.path.basename, cand_list))
            corresponding_img_path = difflib.get_close_matches(
                ann_without_ext, cand_list_no_fileextension, n=1, cutoff=0
            )[0]
            corresponding_img_path = cand_list[
                cand_list_no_fileextension.index(corresponding_img_path)
            ]

        except IndexError:
            print("Cannot find corresponding image file for ", ann, " - Skipped.")
            continue
        index_image = img_names.index(corresponding_img_path)
        img_annot_pairs.append((images[index_image], ann))
    return img_annot_pairs

def find_image_annotation_pairs_by_dir(ann_dir, img_dir):
    if not os.path.exists(ann_dir):
        import sys

        print(
            "Your annotation folder does not exists: ",
            ann_dir,
            " Check your config file!",
        )
        sys.exit(1)

    if not os.path.exists(img_dir):
        import sys

        print(
            "Your image folder does not exists: ", img_dir, " Check your config file!"
        )
        sys.exit(1)


    img_files = []

    # Scan all image filenames
    for root, directories, filenames in os.walk(img_dir, followlinks=True):
        for filename in filenames:
            if filename.endswith(
                ("jpg", "png", "tiff", "tif", "mrc")
            ) and not filename.startswith("."):
                img_files.append(os.path.join(root, filename))

    # Read annotations

    annotations = []
    for root, directories, filenames in os.walk(ann_dir, followlinks=True):
        for ann in sorted(filenames):
            if ann.endswith((".box", ".txt", ".star")) and not ann.startswith("."):
                annotations.append(os.path.join(root,ann))
    img_annot_pairs = find_image_annotation_pairs(annotations,img_files)

    return img_annot_pairs



def parse_annotation(img_annot_pairs, grid_dims=None, anchor_size=None):

    all_imgs = []
    seen_labels = {}
    for filename, boxpath in img_annot_pairs:
        img = {"object": []}
        img["filename"] = filename#img_files[index_image]
        img["boxpath"] = boxpath

        img["img_size"] = imagereader.read_width_height(img["filename"])

        is_helicion_ptcl = is_helicon_with_particle_coords(boxpath)
        is_helicion_eman = is_eman1_helicion(boxpath)
        if is_helicion_ptcl or is_helicion_eman:
            grid_h = grid_dims[1]
            num_patches = grid_dims[2]
            cell_h = img["img_size"][1] / (num_patches * grid_h)

            if is_helicion_ptcl:
                filaments = CoordsIO.read_eman1_helicon(boxpath, int(cell_h))
            else:
                filaments = CoordsIO.read_eman1_filament_start_end(
                    boxpath, int(cell_h)
                )

            for filament in filaments:
                for box in filament.boxes:
                    obj = {}
                    box_xmin = int(box.x)
                    box_width = int(box.w)
                    box_height = int(box.h)
                    box_ymin = img["img_size"][1] - (int(box.y) + box_height)

                    box_xmax = box_xmin + box_width
                    box_ymax = box_ymin + box_height
                    obj["name"] = "particle"
                    obj["xmin"] = box_xmin
                    obj["ymin"] = box_ymin
                    obj["xmax"] = box_xmax
                    obj["ymax"] = box_ymax
                    img["object"] += [obj]
                    if obj["name"] in seen_labels:
                        seen_labels[obj["name"]] += 1
                    else:
                        seen_labels[obj["name"]] = 1
        else:
            if os.stat(boxpath).st_size != 0:
                if boxpath.endswith((".star")):
                    box_width = int(anchor_size)
                    box_height = int(anchor_size)
                    boxes = CoordsIO.read_star_file(boxpath, (box_width + box_height) // 2)
                else:
                    boxes = CoordsIO.read_eman1_boxfile(boxpath)
                for box in boxes:
                    """
                    Box files are written with coordinate system with an origin in the top left corner. 
                    Each box file is specified by the lower left corner of the box and witdh and the hight of the box.
                    This has to be converted to a coordinate system with origin in the botten left corner.
                    """
                    obj = {}
                    box_xmin = int(box.x)
                    box_width = int(box.w)
                    box_height = int(box.h)
                    box_ymin = img["img_size"][1] - (int(box.y) + box_height)

                    box_xmax = box_xmin + box_width
                    box_ymax = box_ymin + box_height
                    obj["name"] = "particle"
                    obj["xmin"] = box_xmin
                    obj["ymin"] = box_ymin
                    obj["xmax"] = box_xmax
                    obj["ymax"] = box_ymax

                    img["object"] += [obj]
                    if obj["name"] in seen_labels:
                        seen_labels[obj["name"]] += 1
                    else:
                        seen_labels[obj["name"]] = 1

        if len(img["object"]) >= 0:
            all_imgs += [img]

    return all_imgs, seen_labels


def is_helicon_with_particle_coords(path):
    try:
        with open(path) as f:
            first_line = f.readline()
            f.close()
        return "#micrograph" in first_line
    except ValueError:
        return False


def is_eman1_helicion(path):
    try:
        if os.stat(path).st_size == 0:
            return False
        box_lines = np.atleast_2d(np.genfromtxt(path))
        return (
            len(box_lines) > 1
            and len(box_lines[0]) == 5
            and box_lines[0][4] == -1
            and box_lines[1][4] == -2
        )
    except ValueError:
        return False
