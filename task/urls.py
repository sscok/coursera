from django.urls import path
from . import views
from django.urls import path
from task import views

urlpatterns = [
  path('result/', views.CSVPageView.as_view(), name='csv_home_page'),
  path('task/',views.form_request),
  path('result/export/', views.write_to_csv, name='output'),
]
