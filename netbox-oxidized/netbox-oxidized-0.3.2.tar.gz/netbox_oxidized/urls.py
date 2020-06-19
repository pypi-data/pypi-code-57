from django.urls import path

from . import views


# Define a list of URL patterns to be imported by NetBox. Each pattern maps a URL to
# a specific view so that it can be accessed by users.
urlpatterns = (
    path('', views.OxidizedNodeListView.as_view(), name='oxidizednode_list'),
    path('node/', views.OxidizedNodeListView.as_view(), name='oxidizednode_list'),
    path('node/add/', views.OxidizedNodeCreateView.as_view(), name='oxidizednode_add'),
    path('node/import/', views.OxidizedNodeListView.as_view(), name='oxidizednode_import'),
    path('node/<int:pk>/', views.OxidizedNodeView.as_view(), name='oxidizednode'),
    path('node/<int:pk>/edit', views.OxidizedNodeEditView.as_view(), name='oxidizednode_edit'),
    path('node/<int:pk>/delete', views.OxidizedNodeDeleteView.as_view(), name='oxidizednode_delete'),
    path('importnode/', views.OxidizedImportNodeListView.as_view(), name='importnode_list'),
    path('importnode/bulk', views.OxidizedImportNodeListView.as_view(), name='importnode_bulk'),
)