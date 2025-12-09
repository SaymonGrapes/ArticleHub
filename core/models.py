import os
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator

from autoslug import AutoSlugField


def generate_image_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{extension}'

    return os.path.join('uploads', 'articles', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name='articles')
    title = models.CharField(max_length=255)
    excerpt = models.CharField(max_length=255, blank=True, default='')
    content = models.TextField()
    slug = AutoSlugField(
        populate_from='title',
        unique=True,
        db_index=True,
        always_update=False
    )

    source_url = models.URLField(null=True, blank=True)

    image_main = models.ImageField(
        null=True,
        blank=True,
        upload_to=generate_image_path,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])

    tags = models.ManyToManyField(Tag, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.author.nickname}'
