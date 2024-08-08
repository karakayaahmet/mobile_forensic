from django.db import models
from django.utils.text import slugify


# Create your models here.

# model for information of phones with adb commands


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Phone(models.Model):
    STATUS_CHOICES = [
        ('Sifreli', 'Şifreli'),
        ('Sifresiz', 'Şifresiz'),
    ]
    OS_CHOICES = [
        ('Android', 'Android'),
        ('IOS', 'IOS'),
        ('HarmonyOS', 'HarmonyOS'),
    ]
    OPERATOR_CHOICES = [
        ('Turkcell', 'Turkcell'),
        ('Vodafone', 'Vodafone'),
        ('Türk Telekom', 'Türk Telekom'),
    ]
    slug = models.SlugField(default="", null=False, unique=True, db_index=True)
    phone_name = models.CharField(max_length=100)
    phone_model = models.CharField(max_length=100)
    phone_status = models.CharField(max_length=100,choices=STATUS_CHOICES,null=True,blank=True)
    phone_os = models.CharField(max_length=100, choices=OS_CHOICES, null=True, blank=True)
    phone_operator = models.CharField(max_length=100, choices=OPERATOR_CHOICES, null=True, blank=True)
    phone_storage = models.CharField(max_length=100, null=True, blank=True)
    phone_battery = models.CharField(max_length=100, null=True, blank=True)
    phone_image = models.ImageField(upload_to='images/', null=True, blank=True)
    phone_slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    phone_date = models.DateTimeField(null=True, blank=True)
    phone_isCompleted = models.BooleanField(default=True, null=True, blank=True)
    phone_isHome = models.BooleanField(default=False, null=True, blank=True)
    phone_isActive = models.BooleanField(default=False, null=True, blank=True)
    phone_isUpdated = models.BooleanField(default=True, null=True, blank=True)
    phone_version_sdk = models.CharField(max_length=100, null=True, blank=True)
    phone_manufacturer = models.CharField(max_length=100, null=True, blank=True)
    phone_hardware = models.CharField(max_length=100, null=True, blank=True)
    phone_platform = models.CharField(max_length=100, null=True, blank=True)
    phone_serial_no = models.CharField(max_length=100, null=True, blank=True)
    phone_product_name = models.CharField(max_length=100, null=True, blank=True)
    phone_brand = models.CharField(max_length=100, null=True, blank=True)
    phone_language = models.CharField(max_length=100, null=True, blank=True)
    phone_boot_completed = models.CharField(max_length=100, null=True, blank=True)
    phone_timezone = models.CharField(max_length=100, null=True, blank=True)
    phone_sms = models.CharField(max_length=100, null=True, blank=True)
    phone_call = models.CharField(max_length=100, null=True, blank=True)
    phone_wifi = models.CharField(max_length=100, null=True, blank=True)
    phone_bluetooth = models.CharField(max_length=100, null=True, blank=True)
    phone_gps = models.CharField(max_length=100, null=True, blank=True)
    phone_network = models.CharField(max_length=100, null=True, blank=True)
    phone_sim = models.CharField(max_length=100, null=True, blank=True)
    phone_battery_status = models.CharField(max_length=100, null=True, blank=True)
    phone_battery_level = models.CharField(max_length=100, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='phones', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.phone_name)
        super().save(*args, **kwargs)


class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.device_id
