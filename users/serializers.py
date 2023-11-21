from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('id',
                'first_name',
                'last_name',
                'email',
                'password',
                're_password',
                'is_superuser',
                'is_staff',
                'date_joined',
                  )

        extra_kwargs = {'password': {'write_only': True},
                        'date_joined': {'read_only': True},
                        'is_superuser': {'read_only': True},
                        'is_staff': {'read_only': True},
                        }


    def validate(self, attrs):
        method = self.context['request'].method
        
        if method == 'POST':
            password = attrs['password']
            re_password = attrs['re_password']
            
            if password != re_password:
                raise serializers.ValidationError(_('Passwords do not match'))
            
        return super().validate(attrs)
    
    
    def create(self, validated_data):
        del validated_data['re_password']
        user = User.objects.create_user(**validated_data)
        
        return user


class UserChangePassworSerializer(serializers.ModelSerializer):
    """
    Serializer for changing a user's password.
    """
    
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True,
                                         validators=[validate_password])
    re_new_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('current_password',
                'new_password',
                're_new_password',
            )
        
        
    def validate(self, attrs):
        user = self.context['request'].user
        
        if not check_password(attrs['current_password'], user.password):
            raise serializers.ValidationError(_('The current password is incorrect'))

        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError(_('The new passwords do not match'))

        return attrs


    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        
        return instance
