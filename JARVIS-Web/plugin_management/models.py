from django.db import models

#I will define the model later
class Plugin(models.Model):
    name = models.CharField(max_length=200)
