from django.db import models

# Create your models here.

#MODEL OF THE LESSOR TABLE IN THE KOYEB DB
class lessor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=255)
    telephone = models.TextField(max_length=9)
    email = models.TextField(max_length=50)
    room_id = models.ForeignKey('rooms', on_delete=models.CASCADE)
    
    def _str_(self):
        return self.name

#MODEL OF THE LESSOR TABLE IN THE KOYEB DB
class rooms(models.Model):
    id = models.AutoField(primary_key=True)
    direction = models.TextField(max_length=255)
    city = models.TextField(max_length=50)
    state = models.TextField(max_length=20)
    rooms = models.TextField(max_length=1)
    bathrooms = models.TextField(max_length=1)
    metters = models.TextField(max_length=1)
    price = models.TextField(max_length=5)
    description = models.TextField(max_length=150)

#MODEL OF THE TENANTS TABLE IN THE KOYEB DB
class tenants(models.Model):
    id = models.AutoField(primary_key=True)
    Names = models.TextField(max_length=255)
    Surnames = models.TextField(max_length=50)
    Age = models.TextField(max_length=20)
    Email = models.TextField(max_length=1)
    Worktimes = models.TextField(max_length=1)
    Schedules = models.TextField(max_length=1)
    Studies_level = models.TextField(max_length=5)
    Pets = models.TextField(max_length=150)
    Cookies = models.TextField(max_length=1)
    Sport = models.TextField(max_length=1)
    Smoking = models.TextField(max_length=5)
    Organized = models.TextField(max_length=150)