# Generated by Django 3.2.4 on 2021-09-15 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210915_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='uploaded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
