# Generated by Django 4.0.5 on 2022-06-13 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gis_app', '0003_city_country_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='country',
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(null=b'I01\n', on_delete=django.db.models.deletion.CASCADE, to='gis_app.country'),
            preserve_default=b'I01\n',
        ),
    ]