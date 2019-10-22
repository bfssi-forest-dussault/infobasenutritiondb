import os
import django
import pandas as pd
import numpy as np
from pathlib import Path
from math import isnan

# Need to do this in order to access the flaim database models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from infobasenutritiondb.api.models import Nutrient, Region, AgeGroup, AdequacyValueReference, \
    IntakeDistributionCoordinates

nutrients = ['Total energy intake (kcal/d)',
             'Magnesium (mg/d)',
             'Linolenic acid (g/d)',
             'Folate (DFE/d)',
             'Riboflavin (mg/d)',
             'Vitamin C (mg/d)',
             'Niacin (NE/d)',
             'Caffeine (mg/d)',
             'Total monounsaturated fats (g/d)',
             'Potassium (mg/d)',
             'Calcium (mg/d)',
             'Percentage of total energy intake from fat',
             'Percentage of total energy intake from monounsaturated fats',
             'Percentage of total energy intake from sugars',
             'Percentage of total energy intake from protein',
             'Phosphorus (mg/d)',
             'Percentage of total energy intake from carbohydrates',
             'Percentage of total energy intake from linolenic acid',
             'Moisture (g/d)',
             'Vitamin A (RAE/d)',
             'Vitamin B6 (mg/d)',
             'Linoleic acid (g/d)',
             'Sodium (mg/d)',
             'Total polyunsaturated fatty acids (g/d)',
             'Protein (g/d)',
             'Naturally occurring folate (mcg/d)',
             'Iron (mg/d)',
             'Total saturated fats (g/d)',
             'Total sugars (g/d)',
             'Vitamin D (mcg/d)',
             'Total fats (g/d)',
             'Thiamin (mg/d)',
             'Percentage of total energy intake from linoleic acid',
             'Cholesterol (mg/d)',
             'Folacin (mcg/d)',
             'Percentage of total energy intake from polyunsaturated fats',
             'Vitamin B12 (mcg/d)',
             'Total carbohydrates (g/d)',
             'Percentage of total energy intake from saturated fats',
             'Zinc (mg/d)',
             'Total dietary fibre (g/d)'
             ]

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


def populate_reference_tables():
    # Populating the reference values in the DB from the constants defined globally in this script

    for n in nutrients:
        if '(' in n:
            nutrient = n.split("(")[0].strip()
            units = n.split("(")[1].replace(")", "").strip()
        else:
            nutrient = n
            units = None
        # print(f"{nutrient}: {units}")

        if units:
            o, c = Nutrient.objects.get_or_create(nutrient=nutrient, units=units)
        else:
            o, c = Nutrient.objects.get_or_create(nutrient=nutrient)
        # print(f"{o} - {c}")

    for r in region_choices_en:
        if r[0] != r[1]:
            o, c = Region.objects.get_or_create(region=r[1], abbreviation=r[0])
        else:
            o, c = Region.objects.get_or_create(region=r[1])
        # print(f"{o} - {c}")

    for a in age_group_choices:
        o, c = AgeGroup.objects.get_or_create(age_group=a[1], abbreviation=a[0])
        # print(f"{o} - {c}")


def populate_adequacy_value_reference_table():
    """ Takes data from source_data csv and dumps to DB """
    source_data = Path(
        "/home/forest/PycharmProjects/CCHSNutritionViz/DistributionData2019Raw/DistributionReferenceValues-EN.csv")
    df = pd.read_csv(source_data)
    df = df.replace(r'^\s*$', np.nan, regex=True)

    for i, row in df.iterrows():
        nutrient = row['Nutrient/Item (unit)']
        nutrient, units = Nutrient.parse_nutrient_string(nutrient)

        nutrient = Nutrient.objects.get(nutrient=nutrient)
        age_group = AgeGroup.objects.get(age_group=row['Age (years)'])
        region = Region.objects.get(region="Canada excluding territories")

        sex = row['Sex'].strip()
        adequacy_type = row['Adequacy-Type']
        adequacy_value = row['Adequacy-Value']
        excess_type = row['Excess-Type']
        excess_value = row['Excess-Value']

        o, c = AdequacyValueReference.objects.get_or_create(
            nutrient=nutrient,
            age_group=age_group,
            region=region,
            sex=sex,
            adequacy_type=adequacy_type,
            adequacy_value=adequacy_value,
            excess_type=excess_type,
            excess_value=excess_value
        )
        # o.delete()
        print(o, c)


def populate_distribution_table():
    """ Takes data from the source_data csv and dumps to DB"""
    source_data = Path(
        "/home/forest/PycharmProjects/CCHSNutritionViz/static/data/distributions-en-all.csv")
    df = pd.read_csv(source_data)
    df = df.replace(r'^\s*$', np.nan, regex=True)
    print(len(df))

    for i, row in df.iterrows():
        nutrient = row['Nutrient/Item (unit)']
        nutrient, units = Nutrient.parse_nutrient_string(nutrient)

        nutrient = Nutrient.objects.get(nutrient=nutrient)
        age_group = AgeGroup.objects.get(age_group=row['Age (years)'])
        region = Region.objects.get(region="Canada excluding territories")

        sex = row['Sex'].strip()
        year = row['Year']
        x = row['x']
        y = row['y']

        adequacy_reference_object = AdequacyValueReference.objects.get(nutrient=nutrient, age_group=age_group,
                                                                       region=region, sex=sex)
        o = IntakeDistributionCoordinates.objects.create(
            nutrient=nutrient,
            year=year,
            region=region,
            sex=sex,
            age_group=age_group,
            x=x,
            y=y,
            adequacy_reference_object=adequacy_reference_object
        )


def clean_nan_values_from_adequacy_reference():
    """
    Reading the values from the spreadsheet into the DB results in some weird parsing of empty cells...
    need to reset these to None manually
    """
    reference_values = AdequacyValueReference.objects.all()

    for x in reference_values:
        if x.adequacy_type == "nan":
            x.adequacy_type = None
            x.save()

        if x.excess_type == "nan":
            x.excess_type = None
            x.save()

        if isnan(x.adequacy_value):
            x.adequacy_value = None
            x.save()

        if isnan(x.excess_value):
            x.excess_value = None
            x.save()


if __name__ == "__main__":
    # populate_reference_tables()
    # populate_adequacy_value_reference_table()
    # populate_distribution_table()

    # o = IntakeDistributionCoordinates.objects.all()
    # for x in tqdm(o):
    #     x.delete()

    # clean_nan_values_from_adequacy_reference()

    pass
