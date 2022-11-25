from rest_framework import serializers
from client_api.models import BeauticianServices
from .models import User,Beautician, Beauticianphoto, Service, Contactus, ServicesPhotos
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .email import send_otp_via_email
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email','password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','is_beautician']

class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=255, style={'input_type' : 'password'}, write_only = True)
    password = serializers.CharField(max_length=255, style={'input_type' : 'password'}, write_only = True)
    def validate(self, attrs):
      current_password = attrs.get('current_password')
      password = attrs.get('password')
      user = self.context.get('user')
      auth = authenticate(email=user.email, password=current_password)
      if auth:
        user.set_password(password)
        user.save()
      else:
        raise serializers.ValidationError('Invalid password')
      return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/auth/reset-password/'+uid+'/'+token
      print('Password Reset Link', link)
      send_otp_via_email(user.email, link)


      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      uid = self.context.get('uid')
      token = self.context.get('token')
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


class UserBeauticianSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  is_beautician = serializers.BooleanField(default=False)
  class Meta:
    fields = ['is_beautician', 'email']

  def validate(self, attrs):
    email = attrs.get('email')

    is_beautician = attrs.get('is_beautician')

    user = User.objects.get(email=email)
    print(user)
    if is_beautician is True:
      user.is_beautician = True
      user.save()
    return super().validate(attrs)

class BeauticianRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
      model = Beautician
      exclude = ['user_id',]

class BeauticianphotoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Beauticianphoto
    fields = '__all__'

  def create(self,validated_data):
    return Beauticianphoto.objects.create(**validated_data)

class ServicesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Service
    fields = ['service_name',]

class ServicesDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Service
    exclude = ['gender','beautician_id']

class ContactusSerializer(serializers.ModelSerializer):
  class Meta:
    model = Contactus
    fields = '__all__'

  def create(self,validated_data):
    return Contactus.objects.create(**validated_data)

class AddServiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Service
    exclude = ['beautician_id']

class BeauticianService(serializers.ModelSerializer):
  class Meta:
    model = BeauticianServices
    fields = '__all__'


class BeauticianSerializer(serializers.ModelSerializer):
    class Meta:
      model = Beautician
      fields =  ['id','first_name',]

class ServicesPhotos(serializers.ModelSerializer):
  class Meta:
    model  = ServicesPhotos
    fields = '__all__'
