# Generated by Django 3.0.4 on 2020-03-31 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0003_image_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='file_type',
            field=models.CharField(default='', max_length=32),
        ),
    ]
