from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.deletion import CASCADE
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

#..........USER MODEL.............................................................
django_user = get_user_model()
#..................................................................................

#.................................................................
class MyPost(models.Model):
    pic = models.ImageField(upload_to = "images",null=True)
    subject = models.CharField(max_length=200)
    cr_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(to=django_user, on_delete=CASCADE,null=True, blank=True)
    def __str__(self):
        return "%s" % self.subject


class Follower(models.Model):
    user = models.ForeignKey(django_user, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(django_user, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"

class MyProfile(models.Model):
    user = models.OneToOneField(django_user, on_delete=models.CASCADE)
    age = models.IntegerField(default=12,validators=[MinValueValidator(12)])
    address = models.TextField( max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20,choices=(("single","single"),("Commited","Commited"),("Married","Married")),null=True,blank=True)
    gender = models.CharField(max_length=20,choices=(("Male","Male"),("Female","Female"),("others","others")),null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    profilepic = models.ImageField(upload_to = "images",null=True)
    



