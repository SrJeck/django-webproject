# Generated by Django 4.0.1 on 2022-02-05 05:52
# Generated by Django 3.1.5 on 2022-02-04 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='COMPANY',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(null=True)),
                ('username', models.TextField(null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('city', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SEEKER',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(null=True)),
                ('username', models.TextField(null=True)),
                ('fullname', models.CharField(max_length=255, null=True)),
                ('experience', models.TextField(null=True)),
                ('about', models.TextField(null=True)),
                ('resume', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='SKILL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skillname', models.TextField(unique=True)),
            ],
        ),
    ]