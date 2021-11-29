from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts import (constants as ac, models as accounts_models)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def validate(self, data):
        data['email'] = data['email'].lower()
        username = data.get('email')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                ac.INVALID_CREDENTIALS, code='authorization')
        else:
            return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = accounts_models.User
        fields = ['id','email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validated_email(self, email):
        email = email.lower()
        if self.instance is not None and self.instance.email != email:
            raise serializers.ValidationError(ac.EMAIL_CANNOT_UPDATE)
        return email

    def create(self, validated_data):
        user = accounts_models.User(email=validated_data['email'],
                                    first_name=validated_data['first_name'],
                                    last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = accounts_models.Group
        fields = ['id','admin', 'title', 'description','users']

    """applying validator so that admin cannot be updated"""
    def validated_admin(self, admin):
        if self.instance is not None and self.instance.admin != admin:
            raise serializers.ValidationError(ac.ADMIN_CANNOT_UPDATE)
        return admin

    """override create method to add admin in the group by default when the group created."""
    def create(self, validated_data):
        admin = self.context["request"].user
        validated_data["admin"] = admin
        if admin not in validated_data["users"]:
            validated_data["users"].append(admin)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "users" in validated_data:
            instance.users.add(*validated_data["users"])
        if "title" in validated_data:
            instance.title = validated_data["title"]
        if "description" in validated_data:
            instance.description = validated_data["description"]
        instance.save()
        return instance


class UserJiraTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = accounts_models.UserJiraToken
        fields = ['user', 'jira_token', 'expiry']
