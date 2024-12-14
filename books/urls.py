from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BookViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Adjusted to match your main urls
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Adjusted to match your main urls
    path('', include(router.urls)),  # Include the router URLs
]