# Generated by Django 3.1.3 on 2021-01-26 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=56)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('todo', models.CharField(max_length=256)),
                ('uid', models.CharField(max_length=128, unique=True)),
                ('is_done', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.user')),
            ],
        ),
    ]