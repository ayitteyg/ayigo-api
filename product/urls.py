

# setting up API router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProductViewSet
from .views import homepage_page_view, login_view, LogoutView, ProductViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')


#path() should not have "products/etc/etc" because the router handles that automatically.
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('homepage', homepage_page_view, name='homepage'),
    path('', include(router.urls)),  # This correctly registers API endpoints
    
    
    # form display views
    #path('products_form', product_form_view, name='products_form'),
]