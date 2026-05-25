from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class AvailableManager(models.Manager):
    """Возвращает только велосипеды со статусом 'Доступен'"""
    def get_queryset(self):
        return super().get_queryset().filter(is_available=Bike.Status.AVAILABLE)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagBike(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

class TechPassport(models.Model):
    serial_number = models.CharField(max_length=50, unique=True, verbose_name="Серийный номер")
    year_of_manufacture = models.IntegerField(verbose_name="Год выпуска", null=True, blank=True)
    mileage = models.IntegerField(default=0, verbose_name="Пробег (км)")
    last_maintenance = models.DateField(verbose_name="Дата последнего ТО", null=True, blank=True)
    battery_health = models.IntegerField(default=100, verbose_name="Заряд батареи (%)", null=True, blank=True)

    class Meta:
        verbose_name = "Технический паспорт"
        verbose_name_plural = "Технические паспорта"

    def __str__(self):
        return f"Паспорт {self.serial_number}"

#Модель для хранения загруженных файлов
class UploadFile(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    name = models.CharField(max_length=255, blank=True, verbose_name="Оригинальное имя")

    def __str__(self):
        return self.name or self.file.name

    class Meta:
        verbose_name = "Загруженный файл"
        verbose_name_plural = "Загруженные файлы"

class Bike(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        AVAILABLE = 1, 'Доступен'
        RENTED = 2, 'В аренде'
        MAINTENANCE = 3, 'На обслуживании'

    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")
    brand = models.CharField(max_length=100, blank=True, verbose_name="Бренд")
    model = models.CharField(max_length=100, blank=True, verbose_name="Модель")
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=100, verbose_name="Цена за час")
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2, default=500, verbose_name="Цена за день")
    address = models.CharField(max_length=255, blank=True, verbose_name="Адрес парковки")
    description = models.TextField(blank=True, verbose_name="Описание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_available = models.IntegerField(choices=Status.choices, default=Status.AVAILABLE, verbose_name="Статус")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='bikes', verbose_name="Категория")
    tags = models.ManyToManyField('TagBike', blank=True, related_name='bikes', verbose_name="Теги")
    tech_passport = models.OneToOneField('TechPassport', on_delete=models.SET_NULL, null=True, blank=True, related_name='bike', verbose_name="Техпаспорт")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='bikes',verbose_name="Автор")

    objects = models.Manager()
    available = AvailableManager()

    # Фото велосипеда
    photo = models.ImageField(
        upload_to='bikes_photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Фото"
    )

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = "Велосипед"
        verbose_name_plural = "Велосипеды"

    def __str__(self):
        return f"{self.brand} {self.model}" if self.brand else self.name

    def get_absolute_url(self):
        return reverse('bike', kwargs={'bike_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


