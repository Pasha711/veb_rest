from django.db import models


class Origin(models.Model):
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    altitude = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.country} - {self.region}"


class Coffee(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight_grams = models.IntegerField(default=250)
    roast_level = models.CharField(max_length=20) # light, medium, dark
    processing_method = models.CharField(max_length=20) # washed, natural, honey
    flavor_notes = models.CharField(max_length=255)
    stock_quantity = models.IntegerField(default=0)
    popularity_score = models.IntegerField(default=0)
    origin = models.ForeignKey(Origin, on_delete=models.RESTRICT, related_name='coffees')

    def __str__(self):
        return self.title
