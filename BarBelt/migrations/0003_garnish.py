# Generated by Django 5.1.5 on 2025-03-19 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BarBelt', '0002_alter_ingredient_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Garnish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.IntegerField(default=4)),
            ],
        ),
    ]
