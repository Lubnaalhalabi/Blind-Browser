from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('run_deeplearning/', views.dl_url_from_view, name='run-deeplearning'),
    path('run_traditional/', views.tr_url_from_view, name='run-traditional'),
    path('run_findnumberofclusters/', views.num_url_from_view, name='run-findnumberofclusters'),
    path('delete_static_files/', views.delete_static_files, name='delete-static-files')
]
