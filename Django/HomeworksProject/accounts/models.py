from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfileManager(models.Manager):
    def get_queryset(self):
        # using resultset from inherited method and customization with e.g. filer
        queryset = super(UserProfileManager, self).get_queryset().filter(city='Praha')
        return queryset

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='', blank=True)
    addres1     = models.CharField(max_length=100, default='', blank=True)
    addres2     = models.CharField(max_length=100, default='', blank=True)
    addres3     = models.CharField(max_length=100, default='', blank=True)
    city        = models.CharField(max_length=100, default='', blank=True)
    state       = models.CharField(max_length=10, default='', blank=True)
    country     = models.CharField(max_length=3, default='', blank=True)
    zip_code    = models.CharField(max_length=10, default='', blank=True)
    phone       = models.CharField(max_length=12, default='', blank=True)
    mobile      = models.CharField(max_length=12, default='', blank=True)
    webSite     = models.URLField(default='', blank=True)
    delivery_addres = models.BooleanField(default=False)
    image       = models.ImageField(upload_to='profile_image', blank=True)
    
    def __str__(self):
        return f'{self.user.username}: {self.user.last_name} {self.user.first_name}'
    
    Praha = UserProfileManager()
    objects = models.Manager() 
    
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
    
    
post_save.connect(create_profile, sender=User)
