from datetime import datetime, timedelta

import uuid as uuid
from django.db import models

from account.models import User


class Restaurant(models.Model):
    city = models.CharField('Город', max_length=100)
    name = models.CharField('Наименование', max_length=100)
    avg_time = models.IntegerField('Среднее время ожидания', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'


class Table(models.Model):
    number = models.IntegerField('Номер столика', null=False, blank=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Ресторан', related_name='tables')
    capacity = models.SmallIntegerField('Вместимость', default=2)

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики ресторана'

    def __str__(self):
        return f'{self.restaurant.name}: {self.number}-{self.capacity}'


class Booking(models.Model):
    WAITING, ACCEPTED, OVERDUE, CANCELLED_BY_USER = range(4)
    STATUSES = (
        (WAITING, 'Ожидает'),  # Было решено выбрать статусы вместо удаления брони для того, чтобы собирать статистику
        (ACCEPTED, 'Выполнено'),  # Так как статистика важна для бизнес процессов, и к тому-же, можно замечать
        (OVERDUE, 'Просрочено'),  # Пользователей, которые бронируют столики и пропускают ужин
        (CANCELLED_BY_USER, 'Отменено пользователем')
    )
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, verbose_name='Номер брони')
    tables = models.ManyToManyField(Table, verbose_name='Забронированные столики')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='Статус', choices=STATUSES, default=WAITING)
    visit_time = models.TimeField('Время брони', null=True, blank=True)
    expired_time = models.TimeField('Время окончания брони', null=True, blank=True)

    def __str__(self):
        return f'{self.user}: {self.visit_time.strftime("%H:%M")}'

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
