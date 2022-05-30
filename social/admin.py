
from django.contrib import admin
from social.models import  MyPost, Follower, MyProfile
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth import get_user_model

# Register your models here.

#  To Customize admin panel

admin.site.register(Follower)
admin.site.register(MyProfile)



class MyPostAdmin(ModelAdmin):
    list_display = ['subject', 'cr_date','uploaded_by']
    search_fields = ['subject', 'cr_date','uploaded_by']
    list_filter = ['cr_date']
admin.site.register(MyPost,MyPostAdmin)

