# Generated by Django 4.2.10 on 2024-02-29 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone_info', '0011_alter_phone_phone_os'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='phone_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
