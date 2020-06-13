from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Data(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=20)
    radius = models.CharField(max_length=10)

    def __str__(self):
        return '{} -  {}'.format(self.title,self.radius)


