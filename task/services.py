import json

import requests
from datetime import datetime as dt
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule
from django_celery_beat.utils import make_aware

from config.settings import TELEGRAM_API
from task.models import Task


def send_tg_message(message, chat_id):
    """    Отправка сообщения в Telegram    """
    params = {
        'text': message,
        'chat_id': chat_id
    }
    try:
        response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_API}/sendMessage', params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


def remind_of_task(task_id):
    """
    Напоминание о выполнении привычки
    """
    task = Task.objects.get(pk=task_id)
    if task.user.chat_id:
        message = f'''Привет!\nНе забудь сегодня выполнить привычку: "{task.action}" в {task.time.strftime("%H:%M")}\n
        Место: {task.place}'''
        send_tg_message(message, task.user.chat_id)


def create_periodic_task(task):
    """
    Создание периодической задачи Celery
    """
    start_time = timezone.now().strftime("%d.%m.%Y") + task.time.strftime(" %H:%M:%S")
    start_time_dt = dt.strptime(start_time, '%d.%m.%Y %H:%M:%S')
    aware_start_time_dt = make_aware(start_time_dt)

    periodicity = {
        1: IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.DAYS),
        2: CrontabSchedule.objects.get_or_create(minute=aware_start_time_dt.strftime("%M"),
                                                 hour=aware_start_time_dt.strftime("%H"),
                                                 day_of_week='1-5'),
        3: CrontabSchedule.objects.get_or_create(minute=aware_start_time_dt.strftime("%M"),
                                                 hour=aware_start_time_dt.strftime("%H"),
                                                 day_of_week='6-7'),
        4: IntervalSchedule.objects.get_or_create(every=7, period=IntervalSchedule.DAYS),
    }

    PeriodicTask.objects.create(
        interval=periodicity[task.periodicity][0] if task.periodicity in (1, 4) else None,
        crontab=periodicity[task.periodicity][0] if task.periodicity in (2, 3) else None,
        name=f'{task.pk}',
        task='tasks.tasks.task_track',
        kwargs=json.dumps({
            'task_id': task.pk,
        }),
        start_time=aware_start_time_dt
    )