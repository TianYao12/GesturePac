from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Data(models.Model):
    name = models.CharField(max_length=200)
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(242)], default=0)
    num_lives = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)], default=3)

    def __str__(self):
        return self.name + " has a score of " + self.score + "and " + self.lives + " lives"
