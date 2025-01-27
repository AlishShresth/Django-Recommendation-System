from django.urls import path
from movies.api import MovieListCreateAPIView, MovieDetailAPIView

app_name = "movies" # Define the application namespace

urlpatterns = [
  path('movies/', MovieListCreateAPIView.as_view(), name='movie-list'),
  path('movies/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
]