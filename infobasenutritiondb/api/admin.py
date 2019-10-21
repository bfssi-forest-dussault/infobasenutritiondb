from django.contrib import admin
from infobasenutritiondb.api import models

# Register your models here.
admin.site.register(models.AdequacyValueReference)
admin.site.register(models.AgeGroup)
admin.site.register(models.IntakeDistributionCoordinates)
admin.site.register(models.Region)
admin.site.register(models.Nutrient)
