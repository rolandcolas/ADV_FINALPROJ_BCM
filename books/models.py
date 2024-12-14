from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Review(models.Model):  # Ensure this is defined properly
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Example rating from 1 to 5
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'Review for {self.book.title} by {self.user.username}'