# Generated by Django 3.1.1 on 2020-11-07 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_word', models.CharField(max_length=150, verbose_name='Слово пользователя')),
                ('bot_word', models.CharField(max_length=250, verbose_name='Слово Бота')),
                ('error_user_word', models.CharField(max_length=250, verbose_name='Не правильное слово')),
            ],
            options={
                'verbose_name': 'Игра в города',
                'verbose_name_plural': 'Игра в города',
            },
        ),
    ]