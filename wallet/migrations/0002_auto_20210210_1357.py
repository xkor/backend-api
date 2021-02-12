# Generated by Django 3.1.6 on 2021-02-10 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='wallet',
            constraint=models.CheckConstraint(check=models.Q(balance__gte=0), name='min_value_0'),
        ),
    ]
