from django.contrib import admin
from .models import POSTS,COMMENT_SECTION,User , FOLLOWERS

admin.site.register(User)
admin.site.register(POSTS)
admin.site.register(COMMENT_SECTION)
admin.site.register(FOLLOWERS)
# Register your models here.
