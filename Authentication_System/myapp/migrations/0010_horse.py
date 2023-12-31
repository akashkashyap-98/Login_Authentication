# Generated by Django 4.2.3 on 2023-08-14 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_developerdefaultdb_developerseconddb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('is_favourite', models.BooleanField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
