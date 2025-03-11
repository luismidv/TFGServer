from django.db import models

# Create your models here.

#MODEL OF THE LESSOR TABLE IN THE KOYEB DB
class Lessor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=255)
    telephone = models.TextField(max_length=9)
    email = models.TextField(max_length=50)
    room_id = models.ForeignKey('rooms', on_delete=models.CASCADE)
    
    def _str_(self):
        return self.name

#MODEL OF THE LESSOR TABLE IN THE KOYEB DB
class Rooms(models.Model):
    id = models.AutoField(primary_key=True)
    direction = models.TextField(max_length=255)
    city = models.TextField(max_length=50)
    state = models.TextField(max_length=20)
    rooms = models.TextField(max_length=100)
    bathrooms = models.TextField(max_length=100)
    metters = models.TextField(max_length=100)
    price = models.TextField(max_length=100)
    description = models.TextField(max_length=150)

#MODEL OF THE TENANTS TABLE IN THE KOYEB DB
class Tenants(models.Model):
    id = models.AutoField(primary_key=True)
    names = models.TextField(max_length=255)
    surnames = models.TextField(max_length=50)
    age = models.TextField(max_length=20)
    email = models.TextField(max_length=100)
    worktimes = models.TextField(max_length=100)
    schedules = models.TextField(max_length=100)
    studies_level = models.TextField(max_length=100)
    pets = models.TextField(max_length=150)
    cookies = models.TextField(max_length=100)
    sport = models.TextField(max_length=100)
    smoking = models.TextField(max_length=100)
    organized = models.TextField(max_length=150)

    def __str__(self):
        return f"{self.names} {self.surnames}"