from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Почта должна быть задана')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    check_phone = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть введён в следующем формате: '+78009999999'. "
                "Допускается количество цифр не более 15.")

    phone = models.CharField(
        validators=[check_phone],
        max_length=17,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Coords(models.Model):
    latitude = models.DecimalField(decimal_places=8, max_digits=10)
    longitude = models.DecimalField(decimal_places=8, max_digits=10)
    height = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"

    def __str__(self):
        return f"{self.latitude}, {self.longitude}, {self.height}"


class PerevalAdded(models.Model):
    CHOICE_STATUS = (
        ("new", 'новый'),
        ("pending", 'модератор взял в работу'),
        ("accepted", 'модерация прошла успешно'),
        ("rejected", 'модерация прошла, информация не принята'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coord = models.ForeignKey(Coords, on_delete=models.CASCADE)

    beauty_title = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255, blank=True, null=True)
    connect = models.TextField(blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    level_winter = models.CharField(max_length=4, blank=True, null=True)
    level_summer = models.CharField(max_length=4, blank=True, null=True)
    level_autumn = models.CharField(max_length=4, blank=True, null=True)
    level_spring = models.CharField(max_length=4, blank=True, null=True)

    status = models.CharField(max_length=30, choices=CHOICE_STATUS, default="new")

    class Meta:
        verbose_name = "Перевал"
        verbose_name_plural = "Перевалы"

    def __str__(self):
        return self.title


class PerevalImage(models.Model):
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE, related_name='images')
    date_added = models.DateTimeField(auto_now_add=True)
    img_path = models.ImageField(upload_to='images/%Y/%m/%d/')

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return self.img_path.name


class PerevalArea(models.Model):
    title = models.CharField(max_length=255)
    id_parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class ActivityType(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
