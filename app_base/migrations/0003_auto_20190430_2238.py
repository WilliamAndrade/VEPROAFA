# Generated by Django 2.1.7 on 2019-05-01 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0002_auto_20190430_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producao',
            name='quantidade',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
    ]