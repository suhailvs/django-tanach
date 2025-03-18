from django.db import models

# Create your models here.

class Word(models.Model):
    """Hebrew word in the Tanach"""
    book = models.IntegerField()
    chapter = models.IntegerField()
    line = models.IntegerField()
    position = models.IntegerField()
    token = models.CharField(max_length=50)
    meaning = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.book} {self.chapter}:{self.line} {self.token}({self.meaning})'

