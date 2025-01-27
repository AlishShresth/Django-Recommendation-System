from movies.models import Movie
from movies.serializers import MovieSerializer
from rest_framework import generics

# For listing all movies and creating a new movie
class MovieListCreateAPIView(generics.ListCreateAPIView):
  queryset = Movie.objects.all().order_by('id')
  serializer_class = MovieSerializer

# For retrieving, updating and deleting a single movie
class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer

  

