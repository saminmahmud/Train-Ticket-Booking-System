from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length= 100)

    def __str__(self) :
        return self.name