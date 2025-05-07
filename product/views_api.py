from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer




# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can post

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)  # Assign logged-in user to the product

#     def get_queryset(self):
#         return Product.objects.filter(user=self.request.user) #restrict users to thier own product



from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Category, User
from .serializers import ProductSerializer, ProductUpdateSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category', 'created_by')
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You don't have permission to edit this product"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], url_path='user/(?P<user_id>[^/.]+)')
    def user_products(self, request, user_id=None):
        """
        Example: /api/products/user/5/
        Returns all products created by user with ID 5
        """
        user = get_object_or_404(User, pk=user_id)
        products = self.queryset.filter(created_by=user)
        
        # Optional: Add filtering by other parameters
        # if category_id := request.query_params.get('category'):
        #     products = products.filter(category_id=category_id)
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)