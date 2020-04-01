from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('status', 3)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', 0)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = UserManager()

    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
        max_length=128,
        verbose_name='Адрес электронной почты',
    )

    status = models.SmallIntegerField(
        default=4,
        verbose_name='Статус',
    )

    last_name = models.CharField(
        null=False,
        blank=False,
        max_length=128,
        verbose_name='Фамилия',
    )

    first_name = models.CharField(
        null=False,
        blank=False,
        max_length=128,
        verbose_name='Имя',
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name='Администратор'
    )

    USERNAME_FIELD = 'email'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def short_name(self):
        return self.first_name
