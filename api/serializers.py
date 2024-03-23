from rest_framework import serializers
from .models import People, ChoiceList, PeopleChoice
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['id', 'user', 'nickname', 'preferred_employment_type', 'location', 'other']

class ChoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceList
        fields = ['id', 'parent', 'choice_type', 'name']

class PeopleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleChoice
        fields = ['id', 'people', 'choice']