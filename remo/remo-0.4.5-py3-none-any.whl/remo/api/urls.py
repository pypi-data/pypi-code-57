from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework_nested import routers
from rest_auth.views import (
    LoginView, LogoutView
)

from remo_app.remo.api.views.demo_access_viewset import DemoAccessViewSet
from remo_app.remo.api.views.feedback_viewset import Feedbacks
from remo_app.remo.api.views.signup_viewset import SignupViewSet
from remo_app.remo.api.views import (
    TaskViewSet,
    CommonClassViewSet,
    DatasetAnnotationSetImageViewSet,
    UserDatasetViewSet,
    DatasetViewSet,
    AnnotationSetTypeViewSet,
    UserDatasetImageViewSet,
    UserDatasetImageAnnotationsViewSet,
    AnnotationSetTagViewSet,
    AnnotationSetImageTagViewSet,
    AnnotationSetImageViewSet,
    TagViewSet,
    # DatasetImageViewSet,
    UserDatasetFolderViewSet,
    UserDatasetContentsViewSet,
    AnnotationSetViewset,
    DatasetAnnotationSetViewSet,
    AutocompleteViewSet,
    # DatasetSearchViewSet,
    AnnotationSetInsightsViewSet,
    FeedbackViewSet,
    UserViewSet
)

router = routers.DefaultRouter()

router.register(r'task', TaskViewSet, basename='task')
router.register(r'annotation-set-type', AnnotationSetTypeViewSet, basename='annotation-set-type')
router.register(r'common-class', CommonClassViewSet, basename='common-class')
router.register(r'dataset', DatasetViewSet, basename='dataset')
router.register(r'user-dataset', UserDatasetViewSet, basename='user-dataset')
router.register(r'annotation-set', AnnotationSetViewset, basename='annotation-set')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'tag', TagViewSet, basename='tag')
# router.register(r'image', DatasetImageViewSet, base_name='dataset-image')
router.register(r'autocomplete', AutocompleteViewSet, basename="annotation-set")
# router.register(r'dataset-search', DatasetSearchViewSet, base_name='dataset-search')

annotation_set_router = routers.NestedSimpleRouter(
    router, r'annotation-set', lookup='annotation_set'
)
# annotation-set/1/tag
annotation_set_router.register(
    r'tag', AnnotationSetTagViewSet, basename='annotationset-tag'
)
# annotation-set/1/image
annotation_set_router.register(
    r'image', AnnotationSetImageViewSet, basename='annotationset-image'
)
# annotation-set/1/insights
annotation_set_router.register(
    r'insights', AnnotationSetInsightsViewSet, basename='annotationset-insights'
)

annotation_set_image_router = routers.NestedSimpleRouter(
    annotation_set_router, r'image', lookup='image'
)
# annotation-set/1/image/1/tag
annotation_set_image_router.register(
    r'tag', AnnotationSetImageTagViewSet, basename='annotationset-image-tag'
)

dataset_router = routers.NestedSimpleRouter(
    router, r'dataset', lookup='dataset'
)
# dataset/1/annotation-set
dataset_router.register(
    r'annotation-set', DatasetAnnotationSetViewSet, basename='dataset-annotationset'
)
dataset_annotation_set_router = routers.NestedSimpleRouter(
    dataset_router, r'annotation-set', lookup='annotation_set'
)
# dataset/1/annotation-set/1/image
dataset_annotation_set_router.register(
    r'image', DatasetAnnotationSetImageViewSet, basename='dataset-annotationset-image'
)

user_dataset_router = routers.NestedSimpleRouter(
    router, r'user-dataset', lookup='user_dataset'
)
# user-dataset/1/images
user_dataset_router.register(
    r'images', UserDatasetImageViewSet, basename='dataset-image'
)
# user-dataset/1/image-annotations
user_dataset_router.register(
    r'image-annotations', UserDatasetImageAnnotationsViewSet, basename='dataset-image-annotations'
)
# user-dataset/1/folders
user_dataset_router.register(
    r'folders', UserDatasetFolderViewSet, basename='dataset-folder'
)
# user-dataset/1/contents
user_dataset_router.register(
    r'contents', UserDatasetContentsViewSet, basename='dataset-contents'
)

urlpatterns = [
    url(r'^rest-auth/login/$', csrf_exempt(LoginView.as_view()), name='rest_login'),
    url(r'^rest-auth/logout/$', csrf_exempt(LogoutView.as_view()), name='rest_logout'),
    url(r'^demo-access/$', csrf_exempt(DemoAccessViewSet.as_view()), name='demo_access'),
    url(r'^signup/$', csrf_exempt(SignupViewSet.as_view()), name='signup'),
    url(r'^user-info/$', csrf_exempt(UserViewSet.as_view()), name='user_info'),
    url(r'^feedbacks/$', Feedbacks.as_view(), name='feedbacks'),
    url(r'^', include(router.urls)),
    url(r'^', include(annotation_set_router.urls)),
    url(r'^', include(annotation_set_image_router.urls)),
    url(r'^', include(dataset_router.urls)),
    url(r'^', include(dataset_annotation_set_router.urls)),
    url(r'^', include(user_dataset_router.urls)),
]
