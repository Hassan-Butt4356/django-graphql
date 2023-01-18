from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    details=models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

