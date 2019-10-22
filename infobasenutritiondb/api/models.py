from django.db import models
from typing import Optional


# Create your models here.
class Nutrient(models.Model):
    """
    TODO: Implement a translation dictionary
    """
    nutrient = models.CharField(max_length=60)
    units = models.CharField(max_length=20)

    @property
    def nutrient_long(self) -> str:
        return f"{self.nutrient} ({self.units})"

    @staticmethod
    def parse_nutrient_string(n: str) -> (str, Optional[str]):
        """
        :param n: raw nutrient string e.g. 'Calcium (mg/d)'
        :return: (nutrient: str, units: str)
        """
        if '(' in n:
            nutrient = n.split("(")[0].strip()
            units = n.split("(")[1].replace(")", "").strip()
        else:
            nutrient = n
            units = None
        return nutrient, units

    def __repr__(self) -> str:
        if self.units is not "":
            return f"{self.nutrient_long}"
        return self.nutrient

    def __str__(self) -> str:
        if self.units is not "":
            return f"{self.nutrient_long}"
        return self.nutrient


class Region(models.Model):
    """
    TODO: Store all the regions + French translations here
    """
    region_choices_en = [
        ('Canada excluding territories', 'Canada excluding territories'),
        ('NL', 'Newfoundland and Labrador'),
        ('PE', 'Prince Edward Island'),
        ('NS', 'Nova Scotia'),
        ('NB', 'New Brunswick'),
        ('QC', 'Quebec'),
        ('ON', 'Ontario'),
        ('MB', 'Manitoba'),
        ('AB', 'Alberta'),
        ('SK', 'Saskatchewan'),
        ('BC', 'British Columbia'),
        ('Atlantic Region', 'Atlantic Region'),
        ('Prairie Region', 'Prairie Region'),
    ]
    region = models.CharField(choices=region_choices_en, max_length=100)
    abbreviation = models.CharField(max_length=3, null=True, blank=True)

    def __repr__(self):
        return f"{self.region}"

    def __str__(self):
        return f"{self.region}"


class AgeGroup(models.Model):
    age_group_choices = [
        ('1-3', '1-3'),
        ('4-8', '4-8'),
        ('9-13', '9-13'),
        ('14-18', '14-18'),
        ('19-30', '19-30'),
        ('31-50', '31-50'),
        ('51-70', '51-70'),
        ('19>', '19 and over'),
        ('71>', '71 and over'),
    ]
    age_group = models.CharField(choices=age_group_choices, max_length=20)
    abbreviation = models.CharField(max_length=5, null=True, blank=True)

    def __repr__(self):
        return f"{self.age_group}"

    def __str__(self):
        return f"{self.age_group}"


class AdequacyValueReference(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    sex_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both')
    ]
    sex = models.CharField(choices=sex_choices, max_length=10)

    adequacy_choices = (
        ('EAR', 'EAR'),
        ('AI', 'AI'),
        ('AMDR - Lower bound', 'AMDR - Lower bound'),
    )
    adequacy_type = models.CharField(choices=adequacy_choices, max_length=20, null=True, blank=True)
    adequacy_value = models.FloatField(null=True)

    excess_choices = (
        ('UL', 'UL'),
        ('CDRR', 'CDRR'),
        ('AMDR - Upper bound', 'AMDR - Upper bound')
    )
    excess_type = models.CharField(choices=excess_choices, max_length=20, null=True, blank=True)
    excess_value = models.FloatField(null=True)

    def __str__(self):
        # This requires a lot of SQL to actually generate
        return f"{self.nutrient}/{self.age_group}/{self.sex} - {self.adequacy_type}:{self.adequacy_value} - {self.excess_type}:{self.excess_value}"


class IntakeDistributionCoordinates(models.Model):
    nutrient = models.CharField(max_length=100)  # TODO: Change to fk referencing NutrientReference table

    year_choices = [
        ("2015", "2015"),
        ("2004", "2004")
    ]
    year = models.CharField(max_length=4, choices=year_choices)

    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    sex_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both')
    ]
    sex = models.CharField(choices=sex_choices, max_length=10)

    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    # Actual (x,y) coordinate to plot on the distribution curve
    x = models.FloatField()
    y = models.FloatField()

    adequacy_reference_object = models.ForeignKey(AdequacyValueReference, on_delete=models.CASCADE)

    @property
    def age_group_value(self):
        return self.age_group.age_group
