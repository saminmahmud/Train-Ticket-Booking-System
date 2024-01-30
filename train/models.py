from django.db import models
from django.core.validators import MaxValueValidator
from passenger.models import UserAccount
from station.models import Station


class Train(models.Model):
    image = models.ImageField(upload_to='train/media/', null=True, blank=True)
    name = models.CharField(max_length=100)
    start_station = models.ForeignKey(Station, related_name="start_station" , null=True, blank=True, on_delete=models.CASCADE)
    end_station =  models.ForeignKey(Station, related_name="end_station" , null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    def __str__(self) :
        return self.name
    
class Seat(models.Model):
    train = models.ForeignKey(Train, null=True, blank=True, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=3)
    active = models.BooleanField(default=False)
    def __str__(self) :
        return f"{self.train.name} - {self.seat_number} - {self.active}"

class Schedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    train_date = models.CharField(max_length=100)

    def __str__(self) :
        return f"{self.train.name} - {self.train_date}"
    
class Review(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='review')
    name = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviews by {self.name}"
    


class AddTrain(models.Model):
    image = models.ImageField(upload_to='train/media/', null=True, blank=True)
    train_name = models.CharField(max_length=30)
    start_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='start_trains')
    end_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='end_trains')
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    total_number_of_seats = models.IntegerField(default=0, validators=[MaxValueValidator(999)])
    train_date = models.CharField(max_length=50)

    def __str__(self):
        return self.train_name
    

    