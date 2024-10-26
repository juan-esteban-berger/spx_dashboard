from django.db import models

class Info(models.Model):
    id = models.BigIntegerField(primary_key=True)
    symbol = models.CharField(max_length=255)
    security = models.CharField(max_length=255)
    gics_sector = models.CharField(max_length=255)
    gics_sub_industry = models.CharField(max_length=255)
    headquarters_location = models.CharField(max_length=255)
    date_added = models.DateField()
    cik = models.IntegerField()
    founded = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'spx"."info_view'
        ordering = ['symbol']


class Prices(models.Model):
    id = models.BigIntegerField(primary_key=True)
    date = models.DateField()
    ticker = models.CharField(max_length=255)
    metric = models.CharField(max_length=255)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'spx"."prices_view'
        ordering = ['date', 'ticker', 'metric']


class Financials(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ticker = models.CharField(max_length=255)
    date = models.DateField()
    variable = models.CharField(max_length=255)
    value = models.FloatField(null=True)  # Changed to allow null values

    class Meta:
        managed = False
        db_table = 'spx"."financials_view'
        ordering = ['ticker', 'date', 'variable']

    def __str__(self):
        return f"{self.ticker} - {self.date} - {self.variable}"
