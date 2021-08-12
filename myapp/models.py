from django.db import models

# Create your models here.

class Dreamreal(models.Model):
    website = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phonenumber = models.IntegerField()
    online = models.ForeignKey('Online', default=1, on_delete=models.CASCADE, db_constraint=False)
    class Meta:
        db_table = 'dreamreal'

class Online(models.Model):
    domain = models.CharField(max_length=30)
    class Meta:
        db_table = 'online'

class Profile(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='static/picture')

    class Meta:
        db_table = "profile"


class Board(models.Model):
    bname = models.CharField(max_length=20, null=False)
    bsubject = models.CharField(max_length=100, null=False)
    bmessage = models.CharField(max_length=200, null=False)

    #def __str__(self):
    #    return self.bsubject

    class Meta:
        db_table = 'board'


# Create your models here.
