# Generated by Django 5.0.2 on 2024-02-27 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FolderApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('folderName', models.CharField(max_length=50)),
                ('storage', models.IntegerField(blank=True, null=True)),
                ('parentFolder', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='FolderModel',
        ),
    ]
