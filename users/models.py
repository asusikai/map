from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ship = models.CharField(null=True,max_length=30) #선박 용도
    ship_name=models.CharField(null=True,max_length=40) #선박명
    tonnage = models.CharField(null=True,max_length=30) # 톤수
    month=models.IntegerField(null=True) #월
    active_sea = models.CharField(null=True,max_length=30) #활동영해
    time_f=models.CharField(null=True, max_length=20) #시간
    my_info=models.CharField(null=True, max_length=100) #전체합
    type_ck=models.IntegerField(default=0) # 알고리즘 돌려서 db저장유무
    my_type=models.JSONField(default=dict) # 알고리즘을 통한 타입

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()