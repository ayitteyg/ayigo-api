from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can post

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Assign logged-in user to the product

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user) #restrict users to thier own product