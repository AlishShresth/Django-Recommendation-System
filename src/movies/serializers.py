from rest_framework import serializers
from .models import Movie

# ModelSerializer
class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = ["id", "title", "genres"]

