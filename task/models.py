from datetime import timedelta

from django.core.validators import MaxValueValidator
from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Task(models.Model):
    PERIODICITY_CHOICES = [
        (1, 'Каждый день'),
        (2, 'Каждый будний день'),
        (3, 'Каждые выходные'),
        (4, 'Каждую неделю')
    ]

    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Создатель привычки")

    place = models.CharField(
        max_length=100,
        verbose_name='Место',
        **NULLABLE,
        help_text='Место, в котором необходимо выполнять привычку.')

    time = models.TimeField(
        verbose_name='Время',
        **NULLABLE,
        help_text='Время, когда необходимо выполнять привычку.')

    action = models.CharField(
        max_length=100,
        verbose_name='Действие',
        **NULLABLE,
        help_text='Действие, которое представляет собой привычка.')

    pleasant_task = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки',
        help_text='Привычка, которую можно привязать к выполнению полезной привычки.')

    related_task = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name='Связанная привычка',
        help_text='Привычка, которая связана с другой привычкой'
    )

    periodicity = models.PositiveIntegerField(
        default=1,
        choices=PERIODICITY_CHOICES,
        verbose_name='Периодичность',
        **NULLABLE,
        help_text='Периодичность выполнения привычки для напоминания в днях.')

    award = models.CharField(
        max_length=100,
        **NULLABLE,
        verbose_name='Вознаграждение ',
        help_text='Чем пользователь должен себя вознаградить после выполнения.')

    duration = models.DurationField(
        verbose_name='Время на выполнение (сек)',
        help_text='Время, которое  потратит пользователь на выполнение привычки.',
        **NULLABLE,
        validators=[MaxValueValidator(timedelta(seconds=120))])

    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности',
        help_text='Другие пользователи могли брать в пример чужие привычки.')

    def __str__(self):
        return f'Я буду {self.action} в {self.time}  {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('pk',)