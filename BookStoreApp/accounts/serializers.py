from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
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


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True,
                                      required=True)
    old_password = serializers.CharField(write_only=True,
                                         required=True)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password2'])
        instance.save()
        return instance


class ResetPasswordRequestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3, required=True)

    class Meta:
        fields = ['email']


class ProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Profile
        fields = '__all__'
