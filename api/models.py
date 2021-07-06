from django.db import models

# Create your models here.
class Word(models.Model):
	document_index = models.IntegerField()
	words = models.CharField(max_length=300)
	frequency = models.IntegerField()