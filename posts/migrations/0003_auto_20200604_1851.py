# Generated by Django 3.0.4 on 2020-06-04 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200425_1511'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',), 'verbose_name': 'Коментар', 'verbose_name_plural': 'Коментарі'},
        ),
    ]
