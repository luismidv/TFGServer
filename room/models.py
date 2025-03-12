from django.db import models

# Create your models here.

#MODEL OF THE LESSOR TABLE IN THE KOYEB DB
class Lessor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=9)
    email = models.CharField(max_length=50)
    room_id = models.ForeignKey('Rooms', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

#MODEL OF THE LESSOR TABLE IN THE KOYEB DB
class Rooms(models.Model):
    
    direction = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    rooms = models.CharField(max_length=100)
    bathrooms = models.CharField(max_length=100)
    metters = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.direction

#MODEL OF THE TENANTS TABLE IN THE KOYEB DB
class Tenants(models.Model):
    id = models.AutoField(primary_key=True)
    names = models.CharField(max_length=255)
    surnames = models.CharField(max_length=50)
    age = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    worktimes = models.CharField(max_length=100)
    schedules = models.CharField(max_length=100)
    studies_level = models.CharField(max_length=100)
    read = models.CharField(max_length=20)
    pets = models.CharField(max_length=150)
    cookies = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    smoking = models.CharField(max_length=100)
    organized = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.names} {self.surnames}"