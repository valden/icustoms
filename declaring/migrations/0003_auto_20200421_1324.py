# Generated by Django 3.0.4 on 2020-04-21 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declaring', '0002_auto_20200415_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goods_name',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='найменування'),
        ),
    ]
