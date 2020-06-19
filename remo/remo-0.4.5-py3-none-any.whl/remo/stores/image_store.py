from remo_app.remo.models import Dataset, DatasetImage, AnnotationSet, NewAnnotation


class ImageStore:

    @staticmethod
    def total_images_in_dataset(dataset_id: int):
        return DatasetImage.objects.filter(dataset_id=dataset_id).count()

    @staticmethod
    def calc_images_without_annotations(annotation_set_id: int):
        annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
        images_with_annotations = NewAnnotation.objects.filter(annotation_set_id=annotation_set_id).count()

        return ImageStore.total_images_in_dataset(annotation_set.dataset.id) - images_with_annotations
