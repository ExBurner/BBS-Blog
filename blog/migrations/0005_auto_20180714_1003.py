# Generated by Django 2.0.6 on 2018-07-14 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180712_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=60, unique=True, verbose_name='文章标题'),
        ),
    ]
