# Generated by Django 2.2.8 on 2019-12-16 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('publisher',), 'verbose_name': 'News', 'verbose_name_plural': 'News'},
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=models.CharField(default=1, help_text='Enter tags for search using whitespaces between', max_length=255),
            preserve_default=False,
        ),
    ]
