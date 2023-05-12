from rest_framework import serializers
from product.models import Category, Product, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class ProductSerializer(serializers.ModelSerializer):
    product_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = 'title id product_reviews price description product_category'.split()


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False)
    price = serializers.FloatField()
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Director does not exist')
        return category_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)
    product_id = serializers.IntegerField()
    stars = serializers.FloatField(min_value=1, max_value=5)

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Director does not exist')
        return product_id
