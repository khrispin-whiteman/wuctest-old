# Generated by Django 4.1.1 on 2023-03-22 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsettings',
            name='staff_username_last_digits_length',
            field=models.IntegerField(blank=True, null=True, verbose_name='Staff Username Last Digits Length'),
        ),
        migrations.AlterField(
            model_name='systemsettings',
            name='student_no_last_digits_length',
            field=models.IntegerField(blank=True, help_text='The number of digits after the date on the student number: YYMMdigits', null=True, verbose_name='Student No. Last Digits Length'),
        ),
    ]
