from rest_framework import serializers
from .models import LinkedInProfile

class LinkedInProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedInProfile
        fields = ['id', 'full_name', 'email', 'location', 'education', 'experience', 'skills']