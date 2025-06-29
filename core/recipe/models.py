from django.db import models
from django.conf import settings

class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2,blank=True)
    description = models.TextField()
    link=models.CharField(max_length=255,blank=True)
    tags=models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Tag(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name