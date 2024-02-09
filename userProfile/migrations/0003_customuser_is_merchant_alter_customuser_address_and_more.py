# Generated by Django 5.0 on 2024-01-27 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0002_customuser_is_active_customuser_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_merchant',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='country',
            field=models.CharField(blank=True, default='USA', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='state',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
