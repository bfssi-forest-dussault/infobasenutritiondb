from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from infobasenutritiondb.api.serializers import UserSerializer, GroupSerializer, \
    IntakeDistributionCoordinatesSerializer, AdequacyValueReferenceSerializer, AgeGroupSerializer
from infobasenutritiondb.api.models import IntakeDistributionCoordinates, AdequacyValueReference, AgeGroup


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class AgeGroupViewset(viewsets.ModelViewSet):
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class IntakeDistributionCoordinatesViewSet(viewsets.ModelViewSet):
    serializer_class = IntakeDistributionCoordinatesSerializer

    # pagination_class = None

    def get_queryset(self):
        """
        Supports URL parameter filtering e.g. ?nutrient=Vitamin%20C&sex=male
        """
        queryset = IntakeDistributionCoordinates.objects.all().order_by('nutrient')
        sex = self.request.query_params.get('sex', None)
        nutrient = self.request.query_params.get('nutrient', None)
        age_group_value = self.request.query_params.get('age_group_value', None)

        if sex is not None:
            queryset = queryset.filter(sex__icontains=sex)
        if nutrient is not None:
            queryset = queryset.filter(nutrient__icontains=nutrient)
        if age_group_value is not None:
            queryset = queryset.filter(age_group__age_group__icontains=age_group_value)
        return queryset


class AdequacyValueReferenceViewSet(viewsets.ModelViewSet):
    queryset = AdequacyValueReference.objects.all()
    serializer_class = AdequacyValueReferenceSerializer
