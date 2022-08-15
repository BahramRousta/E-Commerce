from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Profile


class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'write_only': True}}

    def save(self):
        user = User(
                    email=self.validated_data['email'],
                    username=self.validated_data['username']
                    )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Profile
        fields = '__all__'