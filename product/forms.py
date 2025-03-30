from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']  # Excluding 'user'
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'style': 'resize: none;'}),  # Limit height
        }