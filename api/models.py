from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None,):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    is_beautician = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Beautician(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255,blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    shop_image = models.ImageField(upload_to="images/Shop_image",blank=True, null=True)
    id_proof = models.ImageField(upload_to="images/id_proof",blank=True, null=True)
    shop_name=models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to="images/shop",blank=True, null=True)
    about_us = models.TextField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f'{self.first_name} {self.id}'

gender = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class Service(models.Model):
    type_name = models.CharField(max_length=255)
    beautician_id = models.ForeignKey(Beautician,  on_delete = models.CASCADE,blank=True, null=True)
    service_name = models.CharField(max_length=255,unique=True)
    price = models.IntegerField()
    duration  = models.TimeField()
    gender = models.CharField(choices=gender, max_length=7)

    def __str__(self):
        return self.service_name

class ServicesPhotos(models.Model):
    type_name = models.ManyToManyField(Service, blank=True)
    images =models.ImageField(upload_to="images/services",blank=True, null=True)

class Beauticianphoto(models.Model):
    user_id = models.ForeignKey(Beautician,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/beautician",blank=True, null=True)

    def __str__(self):
        return str(self.user_id)

class Contactus(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField(max_length=255)

    def __str__(self):
        return str(self.first_name)
