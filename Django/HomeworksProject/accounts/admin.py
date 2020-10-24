from django.contrib import admin
from accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',  'user_info', 'city', 'phone', 'webSite')
    
    def user_info(self, obj):
        return obj.description
    
    def get_queryset(self, request):
    # using resultset from inherited method
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        # customization:
        queryset = queryset.order_by('city', 'country')
        return queryset
    # change desctiption heading
    user_info.short_description = 'Info'
    
    
# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.site_header = 'Administration'

