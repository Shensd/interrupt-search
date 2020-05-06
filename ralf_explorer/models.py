from django.db import models

class Interrupt(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.CharField(max_length=3)
    call_number = models.CharField(max_length=40)
    categories = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    registers_json = models.CharField(max_length=2000)
    sections_json = models.CharField(max_length=5000)
