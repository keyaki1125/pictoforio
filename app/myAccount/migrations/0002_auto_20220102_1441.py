# Generated by Django 3.0 on 2022-01-02 05:41

from django.db import migrations, models
import myAccount.models


class Migration(migrations.Migration):

    dependencies = [
        ('myAccount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=myAccount.models.image_directory_path, verbose_name='プロフィール画像'),
        ),
    ]
