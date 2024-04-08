from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


# Create your models here.

class Products(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length = 50)
    category = models.CharField(max_length = 50, default="")
    subcategory = models.CharField(max_length = 50,default="")
    desc = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)
    emailAddress = models.CharField(max_length = 50)
    message = models.CharField(max_length = 500)

    def __str__(self):
        return self.emailAddress

class login(models.Model):
    emailAddress = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)

class register(models.Model):
    name = models.CharField(max_length = 50)
    emailAddress = models.CharField(max_length = 50)
    password = models.CharField(max_length= 50)

    def __str__(self):
        return self.emailAddress


class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None):
    
        user = self.create_user(
            email,
            password=password,
            name = name,
            tc = tc
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

# User Class 

class User(AbstractBaseUser):

        
    class Meta:
        db_table = 'shop_user'
        
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    tc = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", 'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
