from django.db import models

# Create your models here.
class Users_Book(models.Model):
    mail = models.EmailField(null=True, blank=True)
    username = models.CharField(max_length=20, primary_key=True)
    firstname = models.CharField(max_length=30, null=True, blank=True)
    lastname = models.CharField(max_length=30, null=True, blank=True)
    password = models.CharField(max_length=64)
    count_public_book = models.IntegerField()
    desc = models.TextField(max_length=10000, null=True, blank=True)
    def __str__(self):
        return self.username
class Book(models.Model):
    author = models.CharField(max_length=120)
    title = models.CharField(max_length=60, primary_key=True)
    pred = models.TextField(max_length=1000)
    text = models.TextField()
    date = models.DateField(null=True, blank=True, auto_now=True)
    see = models.IntegerField(null=True)
    def __str__(self):
        return self.title
class Commnet(models.Model):
    book = models.CharField(max_length=60)
    author = models.CharField(max_length=120)
    comment = models.CharField(max_length=1500)
    date = models.DateTimeField(null=True, blank=True, auto_now=True)
    def __str__(self):
        return self.comment