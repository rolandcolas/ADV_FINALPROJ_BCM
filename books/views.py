from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book, Genre
from .serializers import BookSerializer, GenreSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Import Q for complex queries
from django.http import JsonResponse  # For handling JSON responses

def index(request):
    # If user is authenticated, redirect to book management view
    if request.user.is_authenticated:
        return redirect('book_management')
    return render(request, 'index.html')  # Render login page if not authenticated

@login_required  # Ensure this view requires login
def book_management(request):
    query = request.GET.get('search', '')  # Get the search query from the GET request
    # Filter books to only include those added by the logged-in user
    books = Book.objects.filter(user=request.user).prefetch_related('review_set')

    if query:
        # Filter books by title or author using case-insensitive search
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    genres = Genre.objects.all()  # Fetch all genres to populate the dropdown
    return render(request, 'book_management.html', {'books': books, 'search_query': query, 'genres': genres})

@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre_id = request.POST.get('genre')
        read_status = request.POST.get('read_status') == 'on'  # Convert checkbox to boolean

        # Create the book instance
        book = Book(user=request.user, title=title, author=author, genre_id=genre_id, read_status=read_status)
        book.save()  # Save the book to the database

        return redirect('book_management')  # Redirect back to book management page

# Your existing viewsets remain unchanged
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]