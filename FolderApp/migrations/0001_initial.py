# Generated by Django 5.0.2 on 2024-02-27 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FolderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folderName', models.CharField(max_length=50)),
                ('storage', models.IntegerField(blank=True, null=True)),
                ('parentFolder', models.IntegerField(default=0)),
            ],
        ),
    ]
