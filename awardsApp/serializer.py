from profiles.models import Profile
from rest_framework import serializers
from .models import Project





class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user','profile_pic','bio', 'gender','location','mobile', 'website', 'github' )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'project_link', 'description', 'technologies', 'project_image','publisher', 'date_published' )