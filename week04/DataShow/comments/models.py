from django.db import models

# Create your models here.


class Comment(models.Model):

    content = models.TextField()
    star = models.IntegerField()
    pub_time = models.DateTimeField()
