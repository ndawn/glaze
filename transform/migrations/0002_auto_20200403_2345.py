# Generated by Django 3.0.4 on 2020-04-03 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transform', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transformationchain',
            name='file',
            field=models.ImageField(max_length=512, upload_to='transformations'),
        ),
    ]