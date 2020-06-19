# try:
#     from remo_app.remo.api.views.feedback_viewset import FeedbackViewSet
# except Exception:
#     import os
#     if os.getenv('DJANGO_SETTINGS_MODULE') == "remo_app.config.standalone.settings":
#         from remo_app.config.standalone.wsgi import application
from remo_app.remo.api.views.feedback_viewset import FeedbackViewSet


from remo_app.remo.api.views.feedback_viewset import FeedbackViewSet
from remo_app.remo.api.views.annotation_set_image_tag_viewset import AnnotationSetImageTagViewSet
from remo_app.remo.api.views.annotation_set_image_viewset import AnnotationSetImageViewSet
from remo_app.remo.api.views.user_dataset_viewset import UserDatasetViewSet
from remo_app.remo.api.views.dataset_viewset import DatasetViewSet
from remo_app.remo.api.views.task_viewset import TaskViewSet
from remo_app.remo.api.views.common_class_viewset import CommonClassViewSet
from remo_app.remo.api.views.dataset_annotation_set_image_viewset import DatasetAnnotationSetImageViewSet
from remo_app.remo.api.views.annotation_set_type_viewset import AnnotationSetTypeViewSet
from remo_app.remo.api.views.user_dataset_image_viewset import UserDatasetImageViewSet
from remo_app.remo.api.views.user_dataset_image_annotations_viewset import \
    UserDatasetImageAnnotationsViewSet
from remo_app.remo.api.views.annotation_set_tag_viewset import AnnotationSetTagViewSet
from remo_app.remo.api.views.tag_viewset import TagViewSet
from remo_app.remo.api.views.user_dataset_folder_viewset import UserDatasetFolderViewSet
from remo_app.remo.api.views.user_dataset_contents_viewset import UserDatasetContentsViewSet
from remo_app.remo.api.views.dataset_annotation_set_viewset import DatasetAnnotationSetViewSet
from remo_app.remo.api.views.annotation_set_viewset import AnnotationSetViewset
from remo_app.remo.api.views.autocomplete_viewset import AutocompleteViewSet
from remo_app.remo.api.views.annotation_set_insights_viewset import AnnotationSetInsightsViewSet
from .user_viewset import UserViewSet
