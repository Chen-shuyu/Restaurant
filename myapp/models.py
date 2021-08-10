from django.db import models

# Create your models here.
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
