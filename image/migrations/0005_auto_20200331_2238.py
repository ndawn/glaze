# Generated by Django 3.0.4 on 2020-03-31 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0004_image_file_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='file_type',
            new_name='extension',
        ),
    ]