from django.db import models
from django.contrib.auth.models import User

class UserPicture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='media')

    def __str__(self):
        return f'{self.user.username} - {self.picture}'
