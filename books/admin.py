from django.contrib import admin
from .models import Genre, Book, Review  # Import the new model

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Review)  # Register the Review model