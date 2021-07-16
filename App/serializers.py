from rest_framework import serializers
from .models import tian1
class tian1Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tian1
        fields = '__all__'
