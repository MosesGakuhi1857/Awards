from django.contrib import admin
from .models import Profile, Project, Rating, Review



# Register your models here.
class UserFollow(admin.ModelAdmin):
    filter_horizontal =('following','followers')


admin.site.register(Profile, UserFollow)
admin.site.register(Project)
admin.site.register(Rating)
admin.site.register(Review)