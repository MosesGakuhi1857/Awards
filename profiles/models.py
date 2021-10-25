from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Profile(models.Model):
    gender_choice = ("Male", "Male"),("Female","Female")
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = CloudinaryField('Profile Pic')
    bio =  models.TextField(blank=True, default='Welcome to my world')
    gender = models.TextField(blank=True, choices=gender_choice)
    location = models.CharField(max_length = 50,blank=True)
    mobile = models.CharField(max_length=18, blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    followers=models.ManyToManyField(User,related_name='followers', blank=True)
    following=models.ManyToManyField(User,related_name='following', blank=True)

    def __str__(self):
        return self.user.username

        
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete() 

    @classmethod
    def update_profile(cls, prof_id, updated_bio):
        profile = cls.objects.filter(id = prof_id).update(bio = updated_bio)
        return profile

# Create your models here.
