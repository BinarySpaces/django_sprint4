# Generated by Django 5.1.5 on 2025-01-27 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Заголовок'),
        ),
    ]
