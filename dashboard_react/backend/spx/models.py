from django.db import models

class Info(models.Model):
    symbol = models.CharField(max_length=255, primary_key=True)  # Set this as primary key
    security = models.CharField(max_length=255)
    gics_sector = models.CharField(max_length=255)
    gics_sub_industry = models.CharField(max_length=255)
    headquarters_location = models.CharField(max_length=255)
    date_added = models.DateField()
    cik = models.IntegerField()
    founded = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'spx"."info'

class Prices(models.Model):
    date = models.DateField()
    ticker = models.CharField(max_length=255)
    metric = models.CharField(max_length=255)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'spx"."prices'

class Financials(models.Model):
    ticker = models.CharField(max_length=255)
    date = models.DateField()
    variable = models.CharField(max_length=255)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'spx"."financials'
