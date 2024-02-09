from rest_framework import serializers
# from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        password = serializers.CharField(write_only=True)

        # model = settings.AUTH_USER_MODEL
        model = User
        fields = ['email', 'firstname', 'lastname', 'phone', 'address', 'city',
                           'state', 'zipcode', 'country', 'picture', 'is_merchant', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate(self, data):
        email = data['email']
        try:
            User.objects.get(email=email)
            if User.DoesNotExist:
                print("user can be registered")
            else:
                raise serializers.ValidationError("Email already exists")
        except Exception as e:
            print('Exception in validation : ', str(e))
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        # The `validate` method is where we can perform any extra validation.
        # In this case, we want to ensure that the email and password are both present.
        email = data['email']
        password = data['password']

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    f"{email} is not a registered email address")

            if not check_password(password, user.password):
                raise serializers.ValidationError("Incorrect password")

        else:
            raise serializers.ValidationError(
                "Must provide email and password")
        return data
