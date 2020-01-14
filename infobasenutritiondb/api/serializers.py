from django.contrib.auth.models import User, Group
from infobasenutritiondb.api import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgeGroup
        fields = '__all__'


class IntakeDistributionCoordinatesSerializer(serializers.HyperlinkedModelSerializer):
    age_group_value = serializers.ReadOnlyField()
    class Meta:
        model = models.IntakeDistributionCoordinates
        fields = ['nutrient', 'year', 'sex', 'age_group_value', 'x', 'y']


class AdequacyValueReferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AdequacyValueReference
        fields = ['adequacy_type', 'adequacy_value', 'excess_type', 'excess_value', 'age_group_id']
