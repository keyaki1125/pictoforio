# Generated by Django 3.0 on 2022-01-12 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myAccount', '0002_auto_20220102_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_guest',
            field=models.BooleanField(default=False, help_text='ゲストユーザーは利用範囲が制限されます。', verbose_name='ゲストステータス'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, verbose_name='ニックネーム'),
        ),
    ]
