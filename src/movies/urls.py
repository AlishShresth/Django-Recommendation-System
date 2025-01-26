from django.urls import path
# from movies.api import MovieAPIView
from movies.api import MovieListCreateAPIView, MovieDetailAPIView

app_name = "movies" # Define the application namespace

urlpatterns = [
  # path("movies/", MovieAPIView.as_view(), name="movie-api"),
  # path("movies/<int:pk>/", MovieAPIView.as_view(), name="movie-api-detail"),
  path('movies/', MovieListCreateAPIView.as_view(), name='movie-list'),
  path('movies/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
]