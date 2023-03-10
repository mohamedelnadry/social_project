

from rest_framework import serializers
from .models import User, UserToken
import re
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate_email(self, value):

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError('Enter a valid email address')
        return value

    def validate_name(self, value):

        if not re.match(r'^[a-zA-Z ]+$', value):
            raise serializers.ValidationError('Name can only contain letters and spaces')
        return value

    def validate_password(self, value):
        if not re.match(r'^[A-Za-z0-9@#$%^&+=]{8,}$', value):
            raise serializers.ValidationError('Password must be at least 8 characters long and contain letters, numbers, and special characters')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ['token','user']


    def update(self, instance, validated_data):

        instance.token = validated_data.get('email', instance.token)
        instance.save()

        return instance


