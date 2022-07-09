# Generated by Django 4.0.6 on 2022-07-09 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('avg_time', models.IntegerField(blank=True, null=True, verbose_name='Среднее время ожидания')),
            ],
            options={
                'verbose_name': 'Ресторан',
                'verbose_name_plural': 'Рестораны',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер столика')),
                ('capacity', models.SmallIntegerField(default=2, verbose_name='Вместимость')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='booking.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Столик',
                'verbose_name_plural': 'Столики ресторана',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, verbose_name='Номер брони')),
                ('status', models.IntegerField(choices=[(0, 'Ожидает'), (1, 'Выполнено'), (2, 'Просрочено'), (3, 'Отменено пользователем')], default=0, verbose_name='Статус')),
                ('visit_time', models.TimeField(blank=True, null=True, verbose_name='Время брони')),
                ('expired_time', models.TimeField(blank=True, null=True, verbose_name='Время окончания брони')),
                ('tables', models.ManyToManyField(to='booking.table', verbose_name='Забронированные столики')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Бронь',
                'verbose_name_plural': 'Брони',
            },
        ),
    ]
