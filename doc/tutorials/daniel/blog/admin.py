from blog.models import *
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    list_display = ('titel', 'date')   
    
admin.site.register(Post, PostAdmin)
