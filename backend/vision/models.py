from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Data_PAC(models.Model):
    name = models.CharField(max_length=200)
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000)], default=0)
    
    def __str__(self):
        return self.name + " has a pac man score of " + self.score 


class Data_FLAP(models.Model):
    name = models.CharField(max_length=200)
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000)], default=0)
    
    def __str__(self):
        return self.name + " has a flappy bird score of " + self.score 