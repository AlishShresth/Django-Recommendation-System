from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db.models import JSONField
import datetime

class Movie(models.Model):
  title = models.CharField(max_length=255)
  genres = models.JSONField(default=list)
  country = models.CharField(max_length=100, blank=True, null=True)
  extra_data = models.JSONField(default=dict)
  release_year = models.IntegerField(
    validators=[
      MinValueValidator(1888),
      MaxValueValidator(datetime.datetime.now().year)
    ], blank=True, null=True
  )
  
  class Meta:
    unique_together = ('title', 'release_year', 'country')
  def __str__(self) -> str:
    return self.title
  
class UserMoviePreferences(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="movie_preferences")
  preferences = JSONField(default=dict, help_text="Stores user preferences for movies like genres, directors, etc.")
  watch_history = JSONField(default=list, help_text="Stores information about movies the user has watched.")

  def __str__(self) -> str:
    return f"{self.user.username}'s Movie Preferences"



