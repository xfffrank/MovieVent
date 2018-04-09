from django.contrib import admin
from .models import Comment, Movie

# Register your models here.
admin.site.register(Comment)
admin.site.register(Movie)

# 修改管理站点标题
admin.site.site_header = "Movie_Vent"