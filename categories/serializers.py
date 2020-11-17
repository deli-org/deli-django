from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    org_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
