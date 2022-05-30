from django.db import models
from django.conf import settings
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL

class Profile(models.Model):

  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics',default='anon.jpg')
    created = models.DateTimeField(auto_now_add=True)

 
    def __str__(self) -> str:
        return self.user.username

