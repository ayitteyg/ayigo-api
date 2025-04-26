
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views import generic
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import ProductForm
from .drive_service import upload_json_to_drive
from .models import Product





# Create your views here.
# def index(request):
#     return HttpResponse("Hello, You're view is rendering..")



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





class ProductFormView(LoginRequiredMixin, FormView):
    template_name = 'page/products_form.html'
    form_class = ProductForm
    login_url = 'login'  # Redirects to login page if not authenticated
    success_url = '/'  # Redirect after successful form submission

    def form_valid(self, form):
        # Assign the logged-in user before saving
        product = form.save(commit=False)
        product.user = self.request.user
        product.save()
        return super().form_valid(form)

product_form_view_0 = ProductFormView.as_view()




class ProductFormView(LoginRequiredMixin, FormView):
    template_name = 'page/products_form.html'
    form_class = ProductForm
    login_url = 'login'  # Redirects to login page if not authenticated
    success_url = '/'  # Redirect after successful form submission

    def form_valid(self, form):
        # Assign the logged-in user before saving
        product = form.save(commit=False)
        product.user = self.request.user
        product.save()

        # Fetch all products and update product.json in Google Drive
        products = list(Product.objects.values())  # Convert QuerySet to list of dictionaries
        upload_json_to_drive("product.json", products)  # Upload or update file in Drive

        return super().form_valid(form)

product_form_view = ProductFormView.as_view()




class ProductFormView(LoginRequiredMixin, FormView):
    template_name = 'page/products_form.html'
    form_class = ProductForm
    login_url = 'login'  # Redirects to login page if not authenticated
    success_url = '/'  # Redirect after successful form submission

    def form_valid(self, form):
        # Assign the logged-in user before saving
        product = form.save(commit=False)
        product.user = self.request.user
        product.save()

product_form_view = ProductFormView.as_view()


