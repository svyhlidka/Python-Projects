from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Post(models.Model):
    post       = models.CharField(max_length=80)
    user       = models.ForeignKey(User, on_delete=None, related_name='creator')
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now_add=True)
#    updated_by = models.ForeignKey(User, on_delete=None,
#                          blank=True,  related_name='updator')
    
   # https://stackoverflow.com/questions/4670783/make-the-user-in-a-model-default-to-the-current-user
   #  def save_model(self, request, instance, form, change):
   #      user = request.user 
   #      instance = form.save(commit=False)
   #      if not change or not instance.user:
   #          instance.user = user
   #      instance.updated_by = user
   #      instance.save()
   # #     form.save_m2m()
   #      return instance
    
    
class Friend(models.Model):
    users = models.ManyToManyField(User) # default includes (User, related_name='friend_set')
    #friend from class lowercase name + '_set'
    current_user = models.ForeignKey(User, related_name='owner',
                                     null=True, on_delete = models.SET_NULL)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)  
        