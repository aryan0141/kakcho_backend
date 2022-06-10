from django.urls import path
from .views import *
urlpatterns = [
    path('', upload_csv, name="upload_csv"),
    path('filter_by_type/<str:fileid>/', filter_by_type, name="filter_by_type"),
    path('filter_by_contentRating/<str:fileid>/', filter_by_contentRating, name="filter_by_contentRating"),
    path('rounded_rating/<str:fileid>/', rounded_rating, name="rounded_rating"),
]
