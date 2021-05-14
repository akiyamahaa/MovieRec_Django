from django.db import models
from django.contrib.auth.models import User
from movie.models import Movie

from django.db.models.signals import post_save

from PIL import Image
from django.conf import settings
import os

# Create your models here.

def user_dir_path(instance,filename):
  profile_avt_name = 'user_{0}/profile.jpg'.format(instance.user.id)
  full_path = os.path.join(settings.MEDIA_ROOT, profile_avt_name)

  if os.path.exists(full_path):
    os.remove(full_path)

  return profile_avt_name



class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  first_name = models.CharField(max_length=50,null=True,blank=True)
  last_name = models.CharField(max_length=50,null=True,blank=True)
  url = models.CharField(max_length=100,null=True,blank=True)
  profile_info = models.TextField(max_length=150,null=True,blank=True)
  created = models.DateField(auto_now_add=True)
  avatar = models.ImageField(upload_to=user_dir_path,blank=True,null=True)

  def save(self,*arg,**kwargs):
    super().save(*arg,**kwargs)
    SIZE_AVT = 250,250

    if self.avatar:
      avt = Image.open(self.avatar.path)
      avt.thumbnail(SIZE_AVT,Image.LANCZOS)
      avt.save(self.avatar.path)

  def __str__(self):
    return self.user.username

def create_user_profile(sender,instance,created,**kwargs):
  if created:
    Profile.objects.create(user=instance)

def save_user_profile(sender,instance,**kwargs):
  instance.profile.save()

post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)




