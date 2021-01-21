from datetime import datetime, timedelta
from time import mktime
from jwt import encode
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

    def get_by_natural_key(self, email):

        return self.get(email=email)


class StudentManager(BaseUserManager):

    def create_student(self, first_name, last_name, email, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')

        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )
        student.set_password(password)
        student.save()

        return student


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, max_length=30, unique=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def token(self):
        dt = datetime.now() + timedelta(days=1)

        token = encode({
            'id': self.pk,
            'exp': int(mktime(dt.timetuple()))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def __str__(self):
        return self.email


class Student(User, PermissionsMixin):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = StudentManager()
