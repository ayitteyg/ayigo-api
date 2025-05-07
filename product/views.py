
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views import generic
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .drive_service import upload_json_to_drive
from .models import Product


from .functions import load_bulk_products
#       load_bulk_products()



class CustomLoginView(LoginView):
    template_name = 'root/login.html'
    redirect_authenticated_user = True
        
    def get_success_url(self):
        return reverse_lazy('homepage')  # Ensure 'homepage' is the correct URL name for HomepageView
login_view = CustomLoginView.as_view()



#custome login 2
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get username from form
        password = request.POST.get('password')  # Get password from form
        
        user = authenticate(request, username=username, password=password)  # Check credentials
        
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('homepage')  # Redirect to homepage
        else:
            messages.error(request, "Invalid username or password")  # Show error message
    
    return render(request, 'root/login.html')




class HomepageView(generic.ListView):
    template_name = 'root/homepage.html'
    context_object_name = 'products'
    login_url = 'login'  # Redirect to login page if not authenticated
    
    def get_queryset(self):
        yr = datetime.today().year
        queryset = { }
                                
        return queryset 
        
homepage_page_view = HomepageView.as_view() 



from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, ProductUpdateSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return []

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_rating(self, request, slug=None):
        product = self.get_object()
        # Add custom rating update logic here
        return Response(...)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by != request.user:
            return Response(
                {"detail": "You don't have permission to edit this product"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

