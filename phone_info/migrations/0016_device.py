# Generated by Django 4.2.10 on 2024-04-16 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone_info', '0015_alter_phone_phone_image_alter_phone_phone_operator_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
            ],
        ),
    ]
