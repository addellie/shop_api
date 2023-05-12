from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.serializer import CategorySerializer, ProductSerializer, ReviewSerializer, CategoryValidateSerializer,\
    ProductValidateSerializer, ReviewValidateSerializer
from product.models import Category, Product, Review
from django.db.models import Avg, Count
import random


@api_view(['GET', 'POST'])
def category_list_and_product_api_view(request):
    if request.method == 'GET':
        categories_with_count = Category.objects.annotate(products_count=Count('product'))
        categories_with_count_data = []
        for category in categories_with_count:
            categories_with_count_data.append({
                'id': category.id,
                'name': category.name,
                'products_count': category.products_count
            })

        data = categories_with_count_data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        return Response(data=CategorySerializer(category).data)


@api_view(['GET', 'PUT', "DELETE"])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Category not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        category.name = request.data.get('name')
        return Response(data=CategorySerializer(category).data)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        data_dict = ProductSerializer(product, many=True).data
        return Response(data=data_dict)
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(title=title, description=description, price=price, category_id=category_id)
        return Response(data=ProductSerializer(product).data)


@api_view(['GET', 'DELETE', 'PUT'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        return Response(data=ProductSerializer(product).data)


@api_view(['GET', 'POST'])
def review_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data_dict = ReviewSerializer(review, many=True).data
        return Response(data=data_dict)
    if request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        text = request.data.get('text')
        product_id = request.data.get('product_id')
        stars = request.data.get('stars')
        review = Review.objects.create(text=text, product_id=product_id, stars=stars)
        return Response(data=ReviewSerializer(review).data)


@api_view(['GET', 'DELETE', 'PUT'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        review.text = request.data.get('text')
        review.product_id = request.data.get('product_id')
        review.stars = request.data.get('stars')
        return Response(data=ReviewSerializer(review).data)


@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()
    data = []
    for product in products:
        reviews = Review.objects.filter(product=product)
        reviews_data = []
        for review in reviews:
            reviews_data.append({
                'comment': review.text,
                'stars': review.stars,
            })
        avg_rating = reviews.aggregate(Avg('stars'))['stars__avg']

        data.append({
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'reviews': reviews_data,
            'rating': round(avg_rating, 2) if avg_rating else None
        })
    return Response(data=data)
