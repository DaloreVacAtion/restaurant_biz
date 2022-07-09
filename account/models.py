from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = PhoneNumberField('Телефон', unique=True, db_index=True)
    name = models.CharField('Имя', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name if self.name else "Имя не установлено"}: {self.phone_number}'

    @property
    def phone_number(self):
        return str(self.username)


class Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField('Сумма чека', max_digits=20, decimal_places=2)
    visit_date = models.DateTimeField('Дата посещения', auto_now_add=True)
    restaurant = models.ForeignKey('booking.Restaurant', on_delete=models.CASCADE, null=True, blank=False,
                                   related_name='receipts')

    def __str__(self):
        return '%s: дата %s, сумма: %s' % (self.user, self.visit_date, self.amount)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
