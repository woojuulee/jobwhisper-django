# Generated by Django 4.1 on 2023-10-17 13:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("board", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=255, unique=True)),
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=128)),
                ("password2", models.CharField(max_length=128)),
            ],
        ),
    ]