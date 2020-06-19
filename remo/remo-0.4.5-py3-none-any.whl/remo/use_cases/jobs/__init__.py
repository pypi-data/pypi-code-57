from .update_dataset_statistics import update_all_datasets_statistics
from .update_annotation_set_statistics import update_all_annotation_sets_statistics
from .update_image_folder_statistics import update_image_folder_statistics
from .update_image_folder_statistics import delete_orphan_images

all_jobs = [
    update_all_datasets_statistics,
    update_all_annotation_sets_statistics,
    update_image_folder_statistics,
    delete_orphan_images
]
