
from rest_framework import serializers
from django.db import transaction
from .models import User,Dropdown,OwnerDetails
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
import re


class UserRegistrationSerializer(serializers.ModelSerializer):

    def validate_contact(self, value):
        if not value:
            raise serializers.ValidationError("Contact field cannot be empty")

        if not value.isdigit():
            raise serializers.ValidationError("Contact field must contain only digits")

        if len(value) != 10:
            raise serializers.ValidationError("Contact field must be exactly 10 digits long")

        return value

    def validate_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email address")
        return value

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only alphabets")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only alphabets")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if len(value) > 15:
            raise serializers.ValidationError("Password must be at atmost 15 characters long")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character")
        return value

    class Meta:
        model = User
        fields = ('id', 'password', 'contact', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
            'contact': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            contact=validated_data['contact'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        return user

class OwnerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerDetails
        fields = '__all__'

class OwnerRegistrationSerializer(serializers.ModelSerializer):
    owner_details = OwnerDetailsSerializer()

    def validate_contact(self, value):
        if not value:
            raise serializers.ValidationError("Contact field cannot be empty")

        if not value.isdigit():
            raise serializers.ValidationError("Contact field must contain only digits")

        if len(value) != 10:
            raise serializers.ValidationError("Contact field must be exactly 10 digits long")

        return value
    
    def validate_O_contact(self, value):
        if not value:
            raise serializers.ValidationError("Contact field cannot be empty")

        if not value.isdigit():
            raise serializers.ValidationError("Contact field must contain only digits")

        if len(value) != 10:
            raise serializers.ValidationError("Contact field must be exactly 10 digits long")

        return value

    def validate_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email address")
        return value

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only alphabets")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only alphabets")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if len(value) > 15:
            raise serializers.ValidationError("Password must be at atmost 15 characters long")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character")
        return value

    class Meta:
        model = User
        fields = ('id', 'password', 'contact', 'first_name', 'last_name', 'email','owner_details')
        extra_kwargs = {
            'password': {'write_only': True},
            'contact': {'required': True},
            'email': {'required': True}
        }

    

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        owner_details_data = validated_data.pop('owner_details')


        print(owner_details_data)
        
        try:
            user = User.objects.create_user(
                contact=validated_data['contact'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                is_staff=True
            )
            OwnerDetails.objects.create(
                user=user, 
                o_contact=owner_details_data['o_contact'],
                address1=owner_details_data['address1'],
                address2=owner_details_data['address2'],
                city=owner_details_data['city'],
                state=owner_details_data['state'],
                zip_code=owner_details_data['zip_code'],
                country=owner_details_data['country'],
                id_proof_type=owner_details_data['id_proof_type'],
                proof_image=owner_details_data['proof_image']
                # proof_image = proof_image

            )
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})
        return user


class LoginSerializer(serializers.Serializer):
    user = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        user = data.get('user')
        if not user:
            raise serializers.ValidationError("Must include 'user and 'password'.")
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    contact = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, data):
        contact = data.get('contact')
        email = data.get('email')
        if not contact and not email:
            raise serializers.ValidationError("Must include either 'contact' or 'email'.")
        return data


class PasswordResetSerializer(serializers.Serializer):
    # token = serializers.CharField()
    new_password = serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if len(value) > 15:
            raise serializers.ValidationError("Password must be at atmost 15 characters long")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'contact', 'gender')


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dropdown 
        fields = ('name', 'order_by')



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    contact_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        contact_or_email = attrs.get('contact_or_email')
        password = attrs.get('password')

        user = User.objects.filter(contact=contact_or_email).first() or User.objects.filter(email=contact_or_email).first()

        if user and user.check_password(password):
            data = super().validate({
                'username': user.contact,  # Pass the contact as username
                'password': password
            })
            data.update({
                'user_id': user.id,
                'email': user.email,
                'contact': user.contact
            })
            return data
        else:
            raise serializers.ValidationError('Invalid credentials')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['contact'] = user.contact
        return token