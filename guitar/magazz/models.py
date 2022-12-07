from django.db import models

# Create your models here.
class Courses(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    vido_path = models.TextField()
