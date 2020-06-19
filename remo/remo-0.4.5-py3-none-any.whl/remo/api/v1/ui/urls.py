from django.conf.urls import url, include
from rest_framework_nested import routers

from remo_app.remo.api.v1.ui.handlers.annotation_set_classes import AnnotationSetClasses
from remo_app.remo.api.v1.ui.handlers.annotation_set_image_annotations import AnnotationSetImageAnnotations
from remo_app.remo.api.v1.ui.handlers.annotation_set_image_status import AnnotationSetImageStatus
from remo_app.remo.api.v1.ui.handlers.annotation_set_image_tags import AnnotationSetImageTags
from remo_app.remo.api.v1.ui.handlers.annotation_set_images import AnnotationSetImages
from remo_app.remo.api.v1.ui.handlers.annotation_set_insights import AnnotationSetInsights
from remo_app.remo.api.v1.ui.handlers.annotation_set_tags import AnnotationSetTags
from remo_app.remo.api.v1.ui.handlers.annotation_sets import AnnotationSets
from remo_app.remo.api.v1.ui.handlers.dataset_annotation_sets import DatasetAnnotationSets
from remo_app.remo.api.v1.ui.handlers.dataset_contents import DatasetContents
from remo_app.remo.api.v1.ui.handlers.dataset_images import DatasetImages
from remo_app.remo.api.v1.ui.handlers.datasets import Datasets
from remo_app.remo.api.v1.ui.handlers.filters import Filters
from remo_app.remo.api.v1.ui.handlers.images import Images
from remo_app.remo.api.v1.ui.handlers.search import SearchView
from remo_app.remo.api.v1.ui.handlers.uploads_status import UploadsStatus

router = routers.DefaultRouter()

router.register(r'datasets', Datasets, basename='datasets')
router.register(r'annotation-sets', AnnotationSets, basename='annotation-sets')
router.register(r'images', Images, basename='images')
router.register(r'search', SearchView, basename='search')
router.register(r'filters', Filters, basename='filters')
router.register(r'uploads', UploadsStatus, basename='uploads')

datasets = routers.NestedSimpleRouter(
    router, r'datasets', lookup='datasets'
)

# datasets/1/contents
datasets.register(
    r'contents', DatasetContents, basename='dataset-contents'
)

# datasets/1/images
datasets.register(
    r'images', DatasetImages, basename='dataset-images'
)

# datasets/1/annotation-sets
datasets.register(
    r'annotation-sets', DatasetAnnotationSets, basename='dataset-annotation-sets'
)

annotation_sets = routers.NestedSimpleRouter(
    router, r'annotation-sets', lookup='annotation_sets'
)

# annotation-sets/1/insights
annotation_sets.register(
    r'insights', AnnotationSetInsights, basename='annotation-sets-insights'
)

# annotation-sets/1/images
annotation_sets.register(
    r'images', AnnotationSetImages, basename='annotation-set-images'
)

annotation_set_images = routers.NestedSimpleRouter(
    annotation_sets, r'images', lookup='images'
)
# annotation-sets/1/images/1/tag
annotation_set_images.register(
    r'tags', AnnotationSetImageTags, basename='annotation-sets-image-tag'
)

# annotation-sets/1/images/1/status
annotation_set_images.register(
    r'status', AnnotationSetImageStatus, basename='annotation-sets-image-status'
)

# annotation-sets/1/images/1/annotations
annotation_set_images.register(
    r'annotations', AnnotationSetImageAnnotations, basename='annotation-sets-image-annotations'
)

# annotation-sets/1/classes
annotation_sets.register(
    r'classes', AnnotationSetClasses, basename='annotation-set-classes'
)

# annotation-sets/1/tags
annotation_sets.register(
    r'tags', AnnotationSetTags, basename='annotation-set-tags'
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(datasets.urls)),
    url(r'^', include(annotation_sets.urls)),
    url(r'^', include(annotation_set_images.urls)),
]
