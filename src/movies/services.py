import csv
import json
import datetime
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from typing import Dict, Any, Tuple, IO
from collections import defaultdict
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from movies.models import Movie, UserMoviePreferences
from movies.serializers import PreferencesSerializer

def add_preference(user_id: int, new_preferences: Dict[str, Any]) -> None:
  """
  Add new preferences or updates existing ones in the user's movie preferences,
  using defaultdict to automatically handle lists and avoiding duplicate entries.
  :param user_id: ID of the user
  :para new_preferences: Dict containing new preferences to be added or updated
  """
  with transaction.atomic():
    user = get_object_or_404(get_user_model(), id=user_id)
    (
      user_preferences, 
      created,
    ) = UserMoviePreferences.objects.select_for_update().get_or_create(
      user_id=user_id, defaults={"preferences": {}}
    )
    # Use defaultdict to automatically handle list creation
    # Convert existing preferences to defaultdict to ease updating
    current_preferences = defaultdict(list, user_preferences.preferences)
    for key, value in new_preferences.items():
      # Ensure value is not already in the list to avoid duplicates
      if value not in current_preferences[key]:
        current_preferences[key].append(value)
    # Convert defaultdict back to dict to ensure compatibility with Django models
    user_preferences.preferences = dict(current_preferences)
    user_preferences.save()
  

def add_watch_history(user_id: int, movie_id: int) -> None:
  """
  Adds a new movie to the user's watch history.
  :param user_id: ID of the user
  :param movie_info: Dict containing information about the movie watched
  """
  movie = get_object_or_404(Movie, id=movie_id)
  movie_info = {
    "title": movie.title,
    "year": movie.release_year,
    "director": movie.extra_data.get("directors", []),
    "genre": movie.genres,
  }
  try:
    with transaction.atomic():
      user_preferences, created = UserMoviePreferences.objects.get_or_create(
        user_id=user_id, defaults={"watch_history": [movie_info]}
      )
  except IntegrityError:
    user_preferences = UserMoviePreferences.objects.get(user_id=user_id)
    created = False
  
  if not created:
    # Add new movie info to existing watch history
    current_watch_history = user_preferences.watch_history
    current_watch_history.append(movie_info)
    user_preferences.watch_history = current_watch_history
    user_preferences.save()

def user_preferences(user_id: int) -> Any:
  user_preferences = get_object_or_404(UserMoviePreferences, user_id=user_id)
  serializer = PreferencesSerializer(user_preferences.preferences)
  return serializer.data

def user_watch_history(user_id: int) -> dict[str, Any]:
  user_preferences = get_object_or_404(UserMoviePreferences, user_id=user_id)
  return {"watch_history": user_preferences.watch_history}

def parse_csv(file: IO[Any]) -> int:
  """
    Parses and processes a CSV file for movie data, cleaning the fields.
  """
  movies_processed = 0
  reader = csv.DictReader(file)
  for row in reader:
    extra_data = row.pop("extra_data").replace("'",'"')
    try:
      extra_data_dict = json.loads(extra_data)
    except json.decoder.JSONDecodeError:
      extra_data_dict = {}
    row["extra_data"] = extra_data_dict
    try:
      row["release_year"] = int(row["release_year"])
    except ValueError:
      continue

    # Clean the fields before passing the movie creation
    row["title"] = clean_text(row["title"])
    row["genres"] = [clean_text(genre) for genre in row["genres"].split(',')]
    row["country"] = clean_text(row["country"])
    create_or_update_movie(**row)
    movies_processed += 1
  return movies_processed

def parse_json(file: IO[Any]) -> int:
  movies_processed = 0
  data = json.load(file)
  for item in data:
    create_or_update_movie(**item)
    movies_processed += 1
  return movies_processed

class FileProcessor:
  def process(self, file_name: str, file_type: str) -> int:
    # check if the file exists in the default storage
    if default_storage.exists(file_name):
      # Open the file directly from storage
      with default_storage.open(file_name, "r") as file:
        if file_type == "text/csv":
          movies_processed = parse_csv(file)
        elif file_type == "application/json":
          movies_processed = parse_json(file)
        else:
          raise ValidationError("Invalid file type")
      return movies_processed
    else:
      raise ValidationError("File does not exist in storage.")

def create_or_update_movie(
    title: str,
    genres: list,
    country: str | None = None,
    extra_data: dict[Any, Any] | None = None,
    release_year: int | None = None
) -> Tuple[Movie, bool]:
  """
    Service function to create or update a Movie instance.
  """
  try:
    # Ensure the release_year is within the acceptable range
    current_year = datetime.datetime.now().year
    if release_year is not None and (release_year < 1888 or release_year > current_year):
      raise ValidationError("The release year must be between 1888 and the current year.")
    
    # Attempt to update an existing movie or create a new one
    movie, created = Movie.objects.update_or_create(
      title=title,
      defaults={
        "genres": genres,
        "country": country,
        "extra_data": extra_data,
        "release_year": release_year,
      }
    )
    return movie, created
  except Exception as e:
    raise ValidationError(f"Failed to create or update the movie: {str(e)}")

# Function to detect strings starting with 'Q' followed by digits
def detect_q_strings(text: str) -> list:
  """
    Detects strings that start with 'Q' followed by digits, useful for cleaning specific formats.
  """
  pattern = r'Q\d+'
  return re.findall(pattern, text)

# Define a function for cleaning text data
def clean_text(text: str) -> str:
  """
    Cleans up the text data by removing punctuation, converting to lowercase,
    removing stopwords, and lemmatizing the text.
  """
  if not isinstance(text, str):
    return ""
  
  # Convert text to lowercase
  text = text.lower()

  # Remove any non-alphanumeric characters, keeping words and digits
  text = re.sub(r'[^a-zA-z0-9\s]', '', text)

  # Tokenize the text into words
  words = word_tokenize(text)

  # Remove stopwords
  stop_words = set(stopwords.words('english'))
  words = [word for word in words if word not in stop_words]

  # Initialize lemmatizer and lemmatize the words
  lemmatizer = WordNetLemmatizer()
  words = [lemmatizer.lemmatize(word) for word in words]

  # Join words back into a cleaned string
  return ' '.join(words)





