from django.db import models

# Create your models here.
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    genre = models.ForeignKey(
        Genre, on_delete = models.CASCADE
    )
    platform = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="games/", blank=True, null=True)

    def __str__(self):
        return self.title