from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import Group

from .models import JournalUser, Article

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        write_only_fields = ('password')
        read_only_fields = ('id',)
        
    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = JournalUser(**data)
        
        # get the password from the data
        password = data.get('password')
        
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)
        
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return super(UserSerializer, self).validate(data)

        
    def create(self, validated_data):

        user = JournalUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        
        my_group = Group.objects.get(name='subscriber') 
        my_group.user_set.add(user)
        user.set_password(validated_data['password'])
        user.save()

        return user

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.email',read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'topic', 'author', 'created_at', 'changed_at','text','for_subscribers')