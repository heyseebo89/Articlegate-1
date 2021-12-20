from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, IntegerField
# Create your models here.
from PIL import Image
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    name = models.CharField(default="User", max_length=25)
    aboutme = models.CharField(default="", max_length=10000)
    phone_no = models.CharField(default="",max_length=13)
    github = models.CharField(default="https://github.com/", max_length=100)
    linkedin = models.CharField(default="https://www.linkedin.com/feed/", max_length=100)
    twitter = models.CharField(default="https://twitter.com/?lang=en", max_length=100)
    instagram = models.CharField(default="https://www.instagram.com/", max_length=100)
    website = models.CharField(default="https://iiitdwd.ac.in/", max_length=100)
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args,**kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (150,150)
            img.thumbnail(output_size)
            img.save(self.image.path)